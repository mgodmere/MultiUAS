import sys

gcs = 20000 # fcu offboard server port (sitl)
fcu_c = 20100 # fcu offboard client port
fcu_s = 20200 # fcu offboard server port (sitl)
mav_udp = 20300 # sim udp server

spacing = 1

def main():
	gazebo = '''
	<arg name="est" default="ekf2"/>
	<arg name="vehicle" default="iris"/>
	<arg name="world" default="$(find mavlink_sitl_gazebo)/worlds/empty.world"/>
	<arg name="gui" default="true"/>
	<arg name="debug" default="false"/>
	<arg name="verbose" default="false"/>
	<arg name="paused" default="false"/>
	<include file="$(find gazebo_ros)/launch/empty_world.launch">
		<arg name="gui" value="$(arg gui)"/>
		<arg name="world_name" value="$(arg world)"/>
		<arg name="debug" value="$(arg debug)"/>
		<arg name="verbose" value="$(arg verbose)"/>
		<arg name="paused" value="$(arg paused)"/>
	</include>
	'''

	uas_template = '''
	<group ns="uas{}">
		<arg name="ID" value="{}"/>
		<arg name="fcu_url" default="udp://:{}@localhost:{}"/>
		<include file="$(find px4)/launch/single_vehicle_spawn.launch">
            <arg name="x" value="{}"/>
            <arg name="y" value="{}"/>
            <arg name="z" value="0"/>
            <arg name="R" value="0"/>
            <arg name="P" value="0"/>
            <arg name="Y" value="0"/>
            <arg name="vehicle" value="$(arg vehicle)"/>
            <arg name="rcS" value="$(find px4)/posix-configs/SITL/init/$(arg est)/$(arg vehicle)_$(arg ID)"/>
            <arg name="mavlink_udp_port" value="{}"/>
            <arg name="ID" value="$(arg ID)"/>
        </include>
		<include file="$(find mavros)/launch/px4.launch">
			<arg name="fcu_url" value="$(arg fcu_url)"/>
			<arg name="gcs_url" value=""/>
			<arg name="tgt_system" value="$(arg ID)"/>
			<arg name="tgt_component" value="1"/>
		</include>
	</group>
	'''

	vehicle_template = '''
		uorb start
		param load
		dataman start
		param set MAV_SYS_ID {}
		param set BAT_N_CELLS 3
		param set CAL_ACC0_ID 1376264
		param set CAL_ACC0_XOFF 0.01
		param set CAL_ACC0_XSCALE 1.01
		param set CAL_ACC0_YOFF -0.01
		param set CAL_ACC0_YSCALE 1.01
		param set CAL_ACC0_ZOFF 0.01
		param set CAL_ACC0_ZSCALE 1.01
		param set CAL_ACC1_ID 1310728
		param set CAL_ACC1_XOFF 0.01
		param set CAL_GYRO0_ID 2293768
		param set CAL_GYRO0_XOFF 0.01
		param set CAL_MAG0_ID 196616
		param set CAL_MAG0_XOFF 0.01
		param set COM_DISARM_LAND 3
		param set COM_OBL_ACT 2
		param set COM_OBL_RC_ACT 0
		param set COM_OF_LOSS_T 5
		param set COM_RC_IN_MODE 1
		param set EKF2_AID_MASK 1
		param set EKF2_ANGERR_INIT 0.01
		param set EKF2_GBIAS_INIT 0.01
		param set EKF2_HGT_MODE 0
		param set EKF2_MAG_TYPE 1
		param set MAV_TYPE 2
		param set MC_PITCH_P 6
		param set MC_PITCHRATE_P 0.2
		param set MC_ROLL_P 6
		param set MC_ROLLRATE_P 0.2
		param set MIS_TAKEOFF_ALT 2.5
		param set MPC_HOLD_MAX_Z 2.0
		param set MPC_Z_VEL_I 0.15
		param set MPC_Z_VEL_P 0.6
		param set NAV_ACC_RAD 2.0
		param set NAV_DLL_ACT 2
		param set RTL_DESCEND_ALT 5.0
		param set RTL_LAND_DELAY 5
		param set RTL_RETURN_ALT 10.0
		param set SDLOG_DIRS_MAX 7
		param set SENS_BOARD_ROT 0
		param set SENS_BOARD_X_OFF 0.000001
		param set SITL_UDP_PRT {}
		param set SYS_AUTOSTART 4010
		param set SYS_MC_EST_GROUP 2
		param set SYS_RESTART_TYPE 2
		replay tryapplyparams
		simulator start -s
		tone_alarm start
		gyrosim start
		accelsim start
		barosim start
		gpssim start
		pwm_out_sim start
		sensors start
		commander start
		land_detector start multicopter
		navigator start
		ekf2 start
		mc_pos_control start
		mc_att_control start
		mixer load /dev/pwm_output0 ROMFS/px4fmu_common/mixers/quad_w.main.mix
		mavlink start -x -u {} -r 4000000
		mavlink start -x -u {} -r 4000000 -m onboard -o {}
		mavlink stream -r 50 -s POSITION_TARGET_LOCAL_NED -u {}
		mavlink stream -r 50 -s LOCAL_POSITION_NED -u {}
		mavlink stream -r 50 -s GLOBAL_POSITION_INT -u {}
		mavlink stream -r 50 -s ATTITUDE -u {}
		mavlink stream -r 50 -s ATTITUDE_QUATERNION -u {}
		mavlink stream -r 50 -s ATTITUDE_TARGET -u {}
		mavlink stream -r 50 -s SERVO_OUTPUT_RAW_0 -u {}
		mavlink stream -r 20 -s RC_CHANNELS -u {}
		mavlink stream -r 250 -s HIGHRES_IMU -u {}
		mavlink stream -r 10 -s OPTICAL_FLOW_RAD -u {}
		logger start -e -t
		mavlink boot_complete
		replay trystart
	'''

	launch = open('launch/sitl_' + sys.argv[1] + '.launch', 'w')
	launch.write('<launch>')
	launch.write(gazebo)

	# clone uav templates
	for i in range(1, int(sys.argv[1]) + 1):
		vehicle_config = open('Firmware/posix-configs/SITL/init/ekf2/iris_' + str(i), 'w')
		x = ((i - 1) * spacing) % 5
		y = ((i - 1) * spacing) / 5
		uas = uas_template.format(
			i,
			i,
			fcu_c + i,
			fcu_s + i,
			x,
			y,
			mav_udp + i
		)

		vehicle = vehicle_template.format(
			i,
			mav_udp + i,
			gcs + i,
			fcu_s + i,
			fcu_c + i,
			gcs + i,
			gcs + i,
			gcs + i,
			gcs + i,
			gcs + i,
			gcs + i,
			gcs + i,
			gcs + i,
			gcs + i,
			gcs + i
		)
		launch.write(uas)
		vehicle_config.write(vehicle)
		vehicle_config.close()

	launch.write('</launch>')
	launch.close()

if __name__ == "__main__":
	main()
