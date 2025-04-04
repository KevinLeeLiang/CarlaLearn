"""
In this script, we are going to learn how to spawn a vehicle on the road and make it autopilot
At the same time, we will collect camera and lidar data from it.
"""
import carla
import os
import random
def main():
    actor_list = []
    sensor_list = []

    try:
        # First of all, we need to create the client that will send the requests, assume port is 2000
        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)
        # Retrieve the world that is currently running
        world = client.get_world()
        blueprint_library = world.get_blueprint_library()
        # Set weather for your world
        weather = carla.WeatherParameters(
            cloudiness=0.0,
            precipitation=0.0,
            fog_density=0.0)
        world.set_weather(weather)

        # create the ego vehicle
        ego_vehicle_bp = blueprint_library.find('vehicle.mercedes.coupe')
        ego_vehicle_bp.set_attribute('color', '0,0,0')
        # get a random valid occupation in the world
        ego_transform = random.choice(world.get_map().get_spawn_points())
        # spawn the ego vehicle
        ego_vehicle = world.spawn_actor(ego_vehicle_bp, ego_transform)
        # set the ego vehicle autopilot mode
        ego_vehicle.set_autopilot(True)

        # collect all actors to destroy when we quit the script
        actor_list.append(ego_vehicle)

        # add a camera to the ego vehicle
        camera_bp = blueprint_library.find('sensor.camera.rgb')
        # camera relative position relative to the ego vehicle
        camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))
        camera = world.spawn_actor(camera_bp, camera_transform, attach_to=ego_vehicle)
        camera.listen(lambda image: image.save_to_disk(os.path.join('images/%06d.png' % image.frame)))
        sensor_list.append(camera)

        # add a lidar to the ego vehicle
        lidar_bp = blueprint_library.find('sensor.lidar.ray_cast')
        lidar_bp.set_attribute('channels', str(32))
        lidar_bp.set_attribute('points_per_second', str(90000))
        lidar_bp.set_attribute('range', str(20))
        lidar_bp.set_attribute('rotation_frequency', str(40))

        # set the lidar relative position relative to the ego vehicle
        lidar_location = carla.Location(0, 0, 2)
        lidar_rotation = carla.Rotation(0, 0, 0)
        lidar_transform = carla.Transform(lidar_location, lidar_rotation)

        # spawn the lidar
        lidar = world.spawn_actor(lidar_bp, lidar_transform, attach_to=ego_vehicle)
        #lidar.listen(lambda point_cloud: point_cloud.save_to_disk('point_clouds/%06d.ply' % point_cloud.frame))
        sensor_list.append(lidar)

        while True:
            # set the sectator to follow the ego vehicle
            speactor = world.get_spectator()
            transform = ego_vehicle.get_transform()

            speactor.set_transform(carla.Transform(transform.location + carla.Location(z=2), transform.rotation))

    finally:
        print('destroying actors')
        client.apply_batch([carla.command.DestroyActor(x) for x in actor_list])
        for sensor in sensor_list:
            sensor.destroy()
        print('done.')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(' - Exited by user.')