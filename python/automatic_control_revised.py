# -*- coding: utf-8 -*-
"""
Revised automatic control
"""
import os
import random
import sys
import carla

from python.agents.navigation.behavior_agent import BehaviorAgent

def main():
    try:
        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)

        # Retrieve the world that is currently running
        world = client.get_world()

        origin_settings = world.get_settings()

        # set sync mode
        settings = world.get_settings()
        settings.synchronous_mode = True
        settings.fixed_delta_seconds = 0.05
        world.apply_settings(settings)

        blueprint_library = world.get_blueprint_library()

        # read all valid spaawn points
        all_defautl_spawn_points = world.get_map().get_spawn_points()
        # randomly choose one as the start point
        spawn_point = random.choice(all_defautl_spawn_points) if all_defautl_spawn_points else carla.Transform()

        # create the blueprint library
        ego_vehicle_bp = blueprint_library.find('vehicle.lincon.mkz2017')
        ego_vehicle_bp.set_attribute('color', '0,0,0')
        # spawn the ego vehicle
        vehicle = world.spawn_actor(ego_vehicle_bp, spawn_point)

        # we need to tick the world once to let the client update the spawn position
        world.tick()

        # create the behavior agent
        """
        Behavior Agent 初始化
        在automatic_control.py里，最重要的不是隶属于Actor class里的vehicle，而是BehaviorAgent class.
        它就像vehicle的大脑，一切指令由它下达，vehicle只管按照这个指令去行走。 
        这个class本身并不是像traffic_manager那样由C++封装好的，它位于PythonAPI/carla/agent中，纯粹由python构成
        
        构建Behavrior Agent Class
        BehavirorAgent在构建时需要两个输入，一个是属于Actor class的Vehicle，另外一个就是车辆驾驶风格（string type）
        """
        agent = BehaviorAgent(vehicle, behavior='normal')

        # set the destination spot
        spawn_points = world.get_map().get_spawn_points()
        random.shuffle(spawn_points)

        # to avoid the destination and start point same
        if spawn_points[0].location != spawn_point.location:
            destination = spawn_points[0]
        else :
            destination = spawn_points[1]

        # generate the route
        """
        全局路径规划
        规划从车辆当前位置到终点为止的路径
        """
        agent.set_destination(agent.vehicle.get_location(), destination.location, clean=True)
        """
        1) world.tick()->仿真世界运行一个步长
        2) agent.update_information(vehicle): BehaviorAgent更新汽车的实时信息，方便更新行为规划
        3) control=agent.run_step(debug=True)->最核心的一步，更新BehaviorAgent的信息后，agent运行新的一步规划，并产生相应的控制命令
        4) vehicle.apply_control(control)->汽车执行产生的控制命令，在仿真世界运行
        """
        while True:
            agent.update_information(vehicle)

            world.tick()

            if len(agent.__local_planner.waypoints_queue) < 1:
                print('======== Success, Arrivied at Target Point!')
                break

            # top view
            spectator = world.get_spectator()
            transform = vehicle.get_transform()
            spectator.set_transform(carla.Transform(transform.location + carla.Location(z=40),
                                                    carla.Rotation(pitch=-90)))

            speed_limit = vehicle.get_speed_limit()
            agent.get_local_planner().set_speed(speed_limit)
            """
            规划一步
            Carla中的规划大致分为五步：
            1）针对交通信号灯的行为规划
            2）针对行人的行为规划
            3）针对路上其他车辆的行为规划
            4）交叉口的行为规划
            5）正常驾驶的行为规划
            """
            control = agent.run_step(debug=True)
            vehicle.apply_control(control)

    finally:
        world.apply_settings(origin_settings)
        vehicle.destroy()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(' - Exited by user.')



