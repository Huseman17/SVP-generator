#!/usr/bin/env python

import math
import matplotlib.pyplot as plt
from tkinter.filedialog import askopenfilename()


# Calculates:   Surface Gravity(m/s)
# Input:        Latitude(degrees)
def calc_surface_gravity(lat):
    sin_rad_lat = math.sin(math.radians(lat))
    gravity = (1 + ((sin_rad_lat ** 2) * .0052788) + ((sin_rad_lat ** 4) * .0000236)) * 9.780318
    # print('surface gravity at', lat, 'deg:', round(gravity, 6), 'm/s^2')
    return gravity


# Calculates: Gravity at depth(m/s^2)
# Input: Surface Gravity(m/s), pressure(dbar)
def calc_gravity_depth(sg, pressure):  # UNESCO Gravity equation
    gravity_depth = .5 * 0.000002184 * pressure + sg
    return gravity_depth


# Calculates: depth(m) UNESCO equation
# Input: pressure, gravity at depth
def calc_depth(pressure, gravity_depth):
    depth1 = (((pressure * 1.45038) * 0.689475728) * 9.72659)
    depth2 = ((((pressure * 1.45038) * 0.689475728) ** 2) * -0.000022512)
    depth3 = ((((pressure * 1.45038) * 0.689475728) ** 3) * .0000000002279)
    depth4 = ((((pressure * 1.45038) * 0.689475728) ** 4) * .00000000000000182)
    depth = (depth1 + depth2 + depth3 + depth4) / gravity_depth
    return depth


def graph(graph_points):
    plt.plot(graph_points[0], graph_points[1])
    plt.ylim(0, len())
    plt.show()


def main():
    sound_vel_dat = open('20200315_28196.000')
    dat_lines = sound_vel_dat.readlines()
    latitude = 28.46
    pressure = 1977.757
    tare = float(dat_lines[21].split()[3][:5])
    fn = dat_lines[3].split('\\')[-1][:-5]
    site = dat_lines[4].split()[3]
    surface_gravity = calc_surface_gravity(latitude)
    sonardyne_pro = open('%s.pro' % fn, 'w')
    sonardyne_pro.write(site)
    sonardyne_pro.write('\n')
    depth_dup_check = 0  # depth_dup_check checks for duplicate pressure readings
    profile_check = 1
    graph_points = [[], []]
    duplicate_count = 0

    for line in dat_lines[28:]:
        pressure = float(line.split()[3])
        sound_velocity = float(line.split()[2])
        gravity_depth = calc_gravity_depth(surface_gravity, pressure)
        depth = calc_depth(pressure, gravity_depth)

        # print('depth', depth, '   DDC', depth_dup_check)
        # print(profile_check, '-', round(depth), '=', profile_check - round(depth), round(depth_dup_check))

        if round(depth) == round(depth_dup_check):
            # print('Duplicate detected:', round(depth))
            duplicate_count += 1
            continue

        sonardyne_pro.write(str(round(depth)))
        sonardyne_pro.write('\t')
        sonardyne_pro.write(str(sound_velocity))
        sonardyne_pro.write('\n')

        graph_points[0].append(sound_velocity)
        graph_points[1].append(round(depth))

        depth_dup_check = depth
        profile_check += 1

    sonardyne_pro.close()

    print('\nREPORT')
    print('Total number of samples collected:', len(dat_lines) - 28)
    print('Number of duplicates:', duplicate_count)
    print('Latitude:', latitude)
    print('Surface Gravity:', round(surface_gravity, 4), 'm/s^2')
    print('Average Sound Velocity:', round(sum(graph_points[0]) / len(graph_points[0]), 3), 'm/s')

    plt.plot(graph_points[0], graph_points[1])
    plt.ylim(len(dat_lines), 0)
    plt.title(site + ' Sound Velocity Profile')
    plt.xlabel('Sound Velocity (m/s)')
    plt.ylabel('Depth (m)')
    plt.show()


main()
