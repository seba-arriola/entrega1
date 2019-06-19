#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import os
from datetime import datetime, timedelta, date, time
import numpy as np
import time


#/home/seba/archive/seisan/REA/GUC__
while(1):
	BASE = raw_input("\nBASE [ex /home/seba/archive/seisan/REA/GUC__/ ] : ")
	BASE = BASE.strip()
	if BASE == "":
		BASE = "/home/seba/archive/seisan/REA/GUC__/"
	if os.path.isdir(BASE):
		if BASE.endswith('/'):
			BASE = BASE[:len(BASE) - 1]
		break
	
	print "invalid directory"


while(1):
	STARTTIME = raw_input("\nSTART TIME [YYYYMMDDHHMMSS] : ")
	STARTTIME = STARTTIME.strip()
	if STARTTIME == "":
		STARTTIME = "20130101000000"
	try:
		STARTTIME = datetime.strptime(STARTTIME, "%Y%m%d%H%M%S")
		break
	except:
		print "invalid date format"
		pass
		
while(1):
	ENDTIME = raw_input("\nEND TIME [YYYYMMDDHHMMSS] : ")
	ENDTIME = ENDTIME.strip()
	if ENDTIME == "":
		ENDTIME=datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')
	try:
		ENDTIME = datetime.strptime(ENDTIME, "%Y%m%d%H%M%S")
		if ENDTIME < STARTTIME:
			print "END TIME must be after START TIME"
			continue
		break
	except:
		print "invalid date format"
		pass
		
		
while(1):
	BOTTOM_LATITUDE = raw_input("\nBOTTOM LATITUDE [-90° to 90°] : ")
	BOTTOM_LATITUDE = BOTTOM_LATITUDE.strip()
	if BOTTOM_LATITUDE == "":
		BOTTOM_LATITUDE = "-90"	
	try:
		BOTTOM_LATITUDE = float(BOTTOM_LATITUDE.strip())
		break
		
	except:
		print "wrong latitude"
		pass
                       

while(1):
	TOP_LATITUDE = raw_input("\nTOP LATITUDE [-90° to 90°] : ")
	TOP_LATITUDE = TOP_LATITUDE.strip()
	if TOP_LATITUDE == "":
		TOP_LATITUDE = "90"		
	try:
		TOP_LATITUDE = float(TOP_LATITUDE.strip())
		if TOP_LATITUDE < BOTTOM_LATITUDE:
			print "TOP LATITUDE must be higher than BOTTOM LATITUDE"
			continue
		break
		
	except:
		print "wrong latitude"
		pass
		
		
while(1):
	LEFT_LONGITUDE= raw_input("\nLEFT LONGITUDE [-180° to 180°] : ")
	LEFT_LONGITUDE=LEFT_LONGITUDE.strip()
	if LEFT_LONGITUDE == "":
		LEFT_LONGITUDE = "-180"
	try:
		LEFT_LONGITUDE = float(LEFT_LONGITUDE.strip())
		break
		
	except:
		print "wrong longitude"
		pass
		
while(1):
	RIGHT_LONGITUDE= raw_input("\nRIGHT LONGITUDE [-180° to 180°] : ")
	RIGHT_LONGITUDE=RIGHT_LONGITUDE.strip()
	if RIGHT_LONGITUDE == "":
		RIGHT_LONGITUDE = "180"
	try:
		RIGHT_LONGITUDE = float(RIGHT_LONGITUDE.strip())
		if RIGHT_LONGITUDE < LEFT_LONGITUDE:
			print "RIGHT LONGITUDE must be higher than LEFT LONGITUDE"
			continue
		break
		
	except:
		print "wrong longitude"
		pass
                    


while(1):
	MIN_DEPTH= raw_input("\nMIN DEPTH [km] : ")
	MIN_DEPTH=MIN_DEPTH.strip()
	if MIN_DEPTH == "":
		MIN_DEPTH="0"
	try:
		MIN_DEPTH = float(MIN_DEPTH.strip())
		break
		
	except:
		print "wrong depth"
		pass
		
		
while(1):
	MAX_DEPTH= raw_input("\nMAX DEPTH [km] : ")
	MAX_DEPTH=MAX_DEPTH.strip()
	if MAX_DEPTH == "":
		MAX_DEPTH="9999"
	try:
		MAX_DEPTH = float(MAX_DEPTH.strip())
		if MAX_DEPTH < MIN_DEPTH:
			print "MAX DEPTH must be higher than MIN DEPTH"
			continue
		break
		
	except:
		print "wrong depth"
		pass
				                

while(1):
	MIN_MAGNITUDE= raw_input("\nMIN MAGNITUDE : ")
	MIN_MAGNITUDE=MIN_MAGNITUDE.strip()
	if MIN_MAGNITUDE == "":
		MIN_MAGNITUDE="0"
	try:
		MIN_MAGNITUDE = float(MIN_MAGNITUDE.strip())
		break
		
	except:
		print "wrong magnitude"
		pass
		
		
while(1):
	MAX_MAGNITUDE= raw_input("\nMAX MAGNITUDE : ")
	MAX_MAGNITUDE=MAX_MAGNITUDE.strip()
	if MAX_MAGNITUDE == "":
		MAX_MAGNITUDE="15"
	try:
		MAX_MAGNITUDE = float(MAX_MAGNITUDE.strip())
		if MAX_MAGNITUDE < MIN_MAGNITUDE:
			print "MAX MAGNITUDE must be higher than MIN MAGNITUDE"
			continue
		break
		
	except:
		print "wrong magnitude"
		pass

while(1):
	try:
		output_filename= raw_input("\nOUTPUT FILENAME : ")
		output_filename=output_filename.strip()
		if output_filename=="":
			output_filename="output"
		try:
			f= open(output_filename,"w+")
		except:
			print "not a valid filename"
			continue
		break
	except:
		pass	
	

station_dict = { } 

d = { }

with open("dict_sta.dat") as f2:
	for line in f2:
		(key, val) = line.split(",")
		d[key] = val.rstrip('\n')

for k in sorted(os.listdir(BASE)):
	
	in_path = BASE+ '/' + str(k)
	try:
		int(k)
	except:
		continue
	
	if datetime.strptime(k,"%Y") < STARTTIME- timedelta(seconds=1):
		continue
	if datetime.strptime(k,"%Y") > ENDTIME:
		break
	

	for dirname in sorted(os.listdir(in_path)):
		if not os.path.isdir(in_path+"/"+dirname):
			continue
		
		if datetime.strptime(k+dirname,"%Y%m") < STARTTIME - timedelta(seconds=1):
			continue
		if datetime.strptime(k+dirname,"%Y%m") > ENDTIME:
			break	
		
		print "\nSearching in %s/%s" %(k,dirname)
		
		for filename in sorted(os.listdir(in_path+"/"+dirname)):
			exists_the_seism=0
			data_file = in_path+"/"+dirname+"/"+filename
			if not data_file.endswith(k+dirname) or not os.path.isfile(data_file):
				continue
				
			data = [line_catalog.rstrip('\n') for line_catalog in open(data_file)]

			#leo la linea con informacion hipocentral
			try:
				linea_sismo = data[0] #si en la linea no hay dato, muera
			except:
				continue
	
			if len(linea_sismo)<80: #si no tiene el tamaño correcto, muera
				continue
			
			try: #valida informacion hipocentral
				year = int(linea_sismo[1:5].strip())
				month = int(linea_sismo[6:8].strip())
				day = int(linea_sismo[8:10].strip())
				hora = int(linea_sismo[11:13].strip())
				minuto = int(linea_sismo[13:15].strip())
				micro_segundos = float(linea_sismo[16:20].strip())
				segundos = int(micro_segundos)
				micro_segundos=int((micro_segundos-float(segundos))*1000000.0)
				o_time= datetime(year, month, day, hora, minuto,segundos,micro_segundos)
				if o_time < STARTTIME:
					continue
				if o_time > ENDTIME:
					break
				latitud = linea_sismo[23:30].strip()
				longitud = linea_sismo[30:38].strip()
				profundidad = linea_sismo[38:43].strip()
				if o_time > datetime(2014, 4, 1, 23, 46,45) and o_time < datetime(2014, 4, 16, 0, 0,1) and latitud>-22 and latitud<-16:
					continue
					
				if o_time > datetime(2015, 9, 16, 22, 54,31) and o_time < datetime(2015, 10, 1, 0, 0,1) and latitud>-35 and latitud<-27:
					continue
			
			except:
				continue

			#si al sismo le falta alguno de sus parametros de localizacion, muera
			if len(latitud)<1 or len(longitud)<1 or len(profundidad)<1:
				continue
			
			if float(latitud)<BOTTOM_LATITUDE or float(latitud)>TOP_LATITUDE:
				continue
			
			if float(longitud)<LEFT_LONGITUDE or float(longitud)>RIGHT_LONGITUDE:
				continue
				
			if float(profundidad)<MIN_DEPTH or float(profundidad)>MAX_DEPTH:
				continue
				
			
			#si no se detecta un problema, el sismo existe
			exists_the_seism = 1
			
			#rms = linea_sismo[51:55].strip()
			
			#lista enlazada para leer las magnitudes
			magnitud=[]
			magnitud1_valor = linea_sismo[55:59].strip()
			magnitud1_tipo = linea_sismo[59].strip()
			if len(magnitud1_valor)>0:
				magnitud.append([magnitud1_valor,magnitud1_tipo])
			magnitud2_valor = linea_sismo[63:67].strip()
			magnitud2_tipo = linea_sismo[67].strip()
			if len(magnitud2_valor)>0:
				magnitud.append([magnitud2_valor,magnitud2_tipo])
			magnitud3_valor = linea_sismo[71:75].strip()
			magnitud3_tipo = linea_sismo[75].strip()
			if len(magnitud3_valor)>0:
				magnitud.append([magnitud3_valor,magnitud3_tipo])
	
	
			#parametros de localizacion del sismo
			linea_aux=""
			ultima_accion=""
			
			error_latitud=""
			error_longitud=""
			error_prof=""
				
			for i in range(1,len(data)):
			
				linea=data[i]
			
				if len(linea)<80:
					continue 
		
				#añadir magnitud csnmag3 en caso de existir
				if linea[73:80]=="CSNMAG3":
					linea_aux=linea.split()
					try:
						float(linea_aux[0])
						magnitud.append([linea_aux[0],linea_aux[1]])
					except:
						print "WARNING: CSNMAG3 magnitude with misformat in file %s\n" %(data_file)
						
				
				if linea[79]=="E":
					linea_a=linea
					error_latitud=linea_a[24:30].strip()
					error_longitud=linea_a[32:38].strip()
					error_prof=linea_a[39:43].strip()
					
				#linea I, informacion del operador
				try:
					if linea[79]=="I":
						linea_aux=linea
						ultima_accion=linea_aux[8:11].strip()
						if ultima_accion=="DUP" or ultima_accion=="REE":
							exists_the_seism = 0
							break

				except:
					continue
			
			
				#parametros especificos en las estaciones para definir el sismo
				if linea[79]=="7":
					starting_param_index = i+1
					break

	
			if exists_the_seism==0:
				continue
			
			the_mags = ""
			good_mag = 0
			for mags in magnitud:
				if float(mags[0])<=MAX_MAGNITUDE and float(mags[0])>=MIN_MAGNITUDE:
					good_mag+=1
				the_mags = the_mags + "%s %s " %(mags[0],mags[1])
			
			if good_mag == 0:
				continue
			
			thisdict =	{ }
			

			for i in range (starting_param_index,len(data)):

				linea_aux = data[i]
				if len( linea_aux.strip() )<1:
					continue
					
				estacion =linea_aux[1:6].strip()

				
				#si la 10 esta vacia, fase larga
				
				if linea_aux[9].strip()=="":
					fase_leida =linea_aux[10:18].strip()
					peso=linea_aux[8].strip()
					ind_calidad=""
					dir_movimiento =""
					
				else:
					try:
						ind_calidad=linea_aux[9].strip()
						fase_leida =linea_aux[10:14].strip()
						peso=linea_aux[14].strip()
						if peso=="4":
							continue
						dir_movimiento =linea_aux[16].strip()
						#time_lectura =linea_aux[18:20].strip()+":"+linea_aux[20:22].strip()+":"+linea_aux[22:28].strip()
						micro_segundos_L = float( linea_aux[22:28].strip() )
						segundos_L = int(micro_segundos_L)
						micro_segundos_L=int((micro_segundos_L-float(segundos_L))*1000000.0)
						time_lectura = datetime(year, month, day, int(linea_aux[18:20].strip()),int(linea_aux[20:22].strip()),segundos_L,micro_segundos_L) 
						diff = (time_lectura-o_time).total_seconds()
						if diff<0:
							continue
						thisdict[estacion+fase_leida] = diff
						residual_tiempo_viaje =linea_aux[63:68].strip()
						peso_rel =linea_aux[68:70].strip()
						distancia_epicentral =linea_aux[70:75].strip()
					except:
						continue
					
				
			
			
			
			for i in range (starting_param_index,len(data)):

				linea_aux = data[i]
				if len( linea_aux.strip() )<1:
					continue
					
				estacion =linea_aux[1:6].strip()
			
				#si la 10 esta vacia, fase larga
				
				if linea_aux[9].strip()=="":
					fase_leida =linea_aux[10:18].strip()
					peso=linea_aux[8].strip()
					if peso=="4":
							continue
					ind_calidad=""
					dir_movimiento =""
					
				else:
					try:
						fase_leida =linea_aux[10:14].strip()
						if fase_leida=="P":
							if estacion+"S" in thisdict:
								final_string="%s %s %s %s %s %.5f %.5f \n" %(latitud, longitud, profundidad, estacion, d[estacion], thisdict[estacion+"P"],thisdict[estacion+"S"])
								final_string=final_string.split()
								f.write( "%s %s %s %s %s %s %s %s %s\n" %( final_string[0],final_string[1],final_string[2],final_string[3],final_string[4],final_string[5],final_string[6],final_string[7],final_string[8] ))
					except:
						continue

f.close()

print "\nSearch finished! Check the results in file: %s\n" %(output_filename)



