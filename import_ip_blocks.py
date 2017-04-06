#!/usr/bin/env python2

import csv
import ipaddress
import mysql.connector
import sys

########################################
# Database settings
########################################

dbUser = "ip-geo"
dbPassword = "changeme#"
dbHost = "localhost"
dbInstance = "ip-geo"
dbTable = "ip_blocks"

########################################
# Script / Procedure
########################################

try:

	filepath=sys.argv[1]

except IndexError:

	print "Usage: ", sys.argv[0], "<path to ip block file>"
	sys.exit(1)

# the useless prefix attached to ipv4 addresses (which are all we care about as of this writing)
ipv4_dumb_prefix = "::ffff:"

# in debug mode?
debug_mode = False

# are we in sample mode (dont process all CSV records)?
sample_mode = False

# sample mode only - define how many rows to read before punting
max_row = 25

# track the row number
row_num = 0

# Database connection
try:

	db_conn = mysql.connector.connect(user=dbUser, password=dbPassword, host=dbHost, db=dbInstance)
	db_cur=db_conn.cursor()	
	print "Connected to", dbUser, "@", dbHost

except mysql.connector.Error as err:

	print "Failed connnecting to", dbUser, "@", dbHost, "-", format(err)
	sys.exit(1)


# open the file and parse it
with open(filepath, 'r') as csv_file:
	
	csv_reader = csv.reader(csv_file)
	
	for row in csv_reader:
		
		row_num += 1
		
		# skip the first line... it's the header
		if row_num == 1:
			continue;		
		
		# Get the IPv4 string-based (dotted quad) address
		ipv6_string_address = row[0]
		ipv4_string_address = ipv6_string_address.replace(ipv4_dumb_prefix, "")
		# Turn it into an object
		ipv4_address = ipaddress.ip_address(unicode(ipv4_string_address))
		# Get the decimal integer representation
		ipv4_dec_start_address = int(ipv4_address)
		
		# Calculate subnet size
		network_mask_length = int(row[1])
		network_num_addresses = 2 ** (128 - network_mask_length)
		
		# Add the decimal subnet size to 
		ipv4_dec_end_address = ipv4_dec_start_address + network_num_addresses
		
		geoname_id = row[2]
		registered_country_geoname_id = row[3]
		represented_country_geoname_id = row[4]
		postal_code = row[5]
		latitude = row[6]
		longitude = row[7]
		is_anonymous_proxy = row[8]
		is_satellite_provider = row[9]
		
		insert_sql = "INSERT INTO `" + dbTable + "` VALUES (" \
					"'" + str(ipv6_string_address) + "', " \
					"'" + str(ipv4_dec_start_address) + "', " \
					"'" + str(ipv4_dec_end_address) + "', " \
					"'" + str(network_mask_length) + "', " \
					"'" + geoname_id + "', " \
					"'" + registered_country_geoname_id + "', " \
					"'" + represented_country_geoname_id + "', " \
					"'" + postal_code + "', " \
					"'" + latitude + "', " \
					"'" + longitude + "', " \
					"'" + is_anonymous_proxy + "', " \
					"'" + is_satellite_provider + "'" \
					")"
		
		if debug_mode:
			print insert_sql		
		
		try:
			db_cur.execute(insert_sql)			
			db_conn.commit()
			print "Inserted:", str(ipv4_dec_start_address), "-", str(ipv4_dec_end_address)
		
		except mysql.connector.Error as err:

			print "Failed to Insert:", str(ipv4_dec_start_address), "-", str(ipv4_dec_end_address), "(" + ipv6_string_address + "/" + str(network_mask_length) + ")", format(err)
			db_conn.rollback()
		
		
		if sample_mode and row_num >= max_row:
			print "stop. hammer time!"
			sys.exit(2)
