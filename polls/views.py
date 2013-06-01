from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import simplejson
from polls.models import User, Patient, Pregnancy, Photo, Doctor, Clinic, Officer, Serve, Works_On, Validation, Comment
from django.views.decorators.csrf import csrf_exempt
import datetime
import time
from django.db.models import Max, Q

def index(request):
	latest_poll_list = User.objects.all()[:5]
	polls_json = []
	for poll in latest_poll_list:
		polls_json.append({
			'name': poll.name,
		})
	return HttpResponse(simplejson.dumps(polls_json), mimetype="application/json")
	
def detail(request, poll_id):
	poll = get_object_or_404(Poll, pk=poll_id)
	return render(request, 'polls/detail.html', {'poll':poll})
	
def results(request, poll_id):
	return HttpResponse("Results Page. You are looking at poll_id: %s" % poll_id)
	
def vote(request, poll_id):
	return HttpResponse("Vote Page. You are looking at poll_id: %s"% poll_id)

@csrf_exempt
def update(request, timestamp):
	print 'Hello'
	json_data = request.read()
	data = simplejson.loads(json_data)
	current_date = datetime.datetime.now()
	current_timestamp = long(time.mktime(current_date.timetuple()))
	
	print data['timestamp']
	
	###Handle Add Operation
	#Condition: add if only if KTP is not exist
	for a in data['add']['user']:
		try:
			temp = User.objects.get(ktp=a['local_ktp'])
		except User.DoesNotExist:
			u = User(
				ktp = a['local_ktp'],
				username = a['username'],
				password = a['password'],
				name = a['name'],
				address = a['address'],
				email = a['email'],
				phone = a['phone'],
				description = a['description'],
				is_active = a['is_active'],
				modify_timestamp = a['modify_timestamp'],
				create_timestamp = a['create_timestamp'],
				server_arrival_timestamp = current_timestamp,
				server_modify_timestamp = current_timestamp,);
			u.save()
			print 'saving user', u.ktp
			
	#Condition: add if only if KTP is not exist
	for a in data['add']['patient']:
		try:
			temp = Patient.objects.get(ktp=a['local_ktp'])
		except Patient.DoesNotExist:
			p = Patient(
				ktp=a['local_ktp'],
				name=a['name'],
				address=a['address'],
				phone=a['phone'],
				birthdate=a['birthdate'],
				filename=a['filename'],
				description=a['description'],
				is_active =a['is_active'],
				modify_timestamp =a['modify_timestamp'],
				create_timestamp =a['create_timestamp'],
				server_arrival_timestamp = current_timestamp,
				server_modify_timestamp = current_timestamp,)
			p.save()
			print 'saving patient', p.ktp	
	
	#Condition: add if only if Patient's KTP+Pregnancy Number is not exist
	for a in data['add']['pregnancy']:
		try:
			temp = Pregnancy.objects.get(patient__ktp=a['local_patient_id'], pregnancy_number=a['local_pregnancy_number'])
		except Pregnancy.DoesNotExist:
			patient_temp = Patient.objects.get(ktp=a['local_patient_id'])
			p = Pregnancy(
				patient=patient_temp,
				pregnancy_number=a['local_pregnancy_number'],
				is_finish=a['is_finish'],
				is_active=a['is_active'],
				modify_timestamp=a['modify_timestamp'],
				create_timestamp=a['create_timestamp'],
				server_arrival_timestamp = current_timestamp,
				server_modify_timestamp = current_timestamp,)
			p.save()
			print 'saving pregnancy', p.patient.ktp, p.pregnancy_number
	
	#Condition: Add if only if no doctor with identical ktp or id
	for a in data['add']['doctor']:
		temp = Doctor.objects.filter(Q(user__ktp=a['local_ktp']) | Q(doctor_id=a['doctor_id']))
		if len(temp) < 1:
			u = User.objects.get(ktp=a['local_ktp'])
			d = Doctor(
				user=u,
				doctor_id=a['doctor_id'],
				is_active=a['is_active'],
				modify_timestamp=a['modify_timestamp'],
				create_timestamp=a['create_timestamp'],
				server_arrival_timestamp = current_timestamp,
				server_modify_timestamp = current_timestamp,)
			d.save()
			print 'saving doctor', d.user.ktp, d.doctor_id
	

	#Condition: Add if only if no identical clinic id exist
	for a in data['add']['clinic']:
		try:
			temp = Clinic.objects.get(clinic_id=a['local_clinic_id'])
		except Clinic.DoesNotExist:		
			c = Clinic(
				clinic_id=a['local_clinic_id'],
				name=a['name'],
				address=a['address'],
				city=a['city'],
				province=a['province'],
				phone=a['phone'],
				description=a['description'],
				is_active=a['is_active'],
				modify_timestamp=a['modify_timestamp'],
				create_timestamp=a['create_timestamp'],
				server_arrival_timestamp = current_timestamp,
				server_modify_timestamp = current_timestamp,)
			c.save()
			print 'saving clinic', c.clinic_id
			
	#Condition: Add if only if no officer with identical ktp or id
	for a in data['add']['officer']:
		temp = Officer.objects.filter(Q(user__ktp=a['local_ktp']) | Q(officer_id=a['officer_id']))
		if len(temp) == 0 :
			u = User.objects.get(ktp=a['local_ktp'])
			o = Officer(
				user=u,
				officer_id=a['officer_id'],
				clinic_id=a['local_clinic_id'],
				is_active=a['is_active'],
				modify_timestamp=a['modify_timestamp'],
				create_timestamp=a['create_timestamp'],
				server_arrival_timestamp = current_timestamp,
				server_modify_timestamp = current_timestamp,)
			o.save()
			print 'saving officer', o.user.ktp, o.officer_id
	
	photo_confirmation = []
	#Condition: Add as long as KTP + Pregnancy exist. Global photo number may be differ
	for a in data['add']['photo']:
		try:
			temp = Pregnancy.objects.get(patient__ktp=a['local_ktp'], pregnancy_number=a['local_pregnancy_number'])
			o = Officer.objects.get(user__ktp=a['local_officer_ktp'])
			last_objects = Photo.objects.filter(pregnancy__pregnancy_id=temp.pregnancy_id).aggregate(Max('photo_number'))
			last_number = last_objects['photo_number__max']
			if  last_number is None:
				last_number = 1
			p = Photo(
				pregnancy=temp,
				officer = o,
				photo_number=last_number + 1,
				analyze_timestamp=a['analyze_timestamp'],
				filename=a['filename'],
				x=a['x'],
				y=a['y'],
				a=a['a'],
				b=a['b'],
				tetha=a['tetha'],
				scale=a['scale'],
				method=a['method'],
				is_active=a['is_active'],
				modify_timestamp=a['modify_timestamp'],
				create_timestamp=a['create_timestamp'],
				server_arrival_timestamp = current_timestamp,
				server_modify_timestamp = current_timestamp,)
			p.save()
			photo_confirmation.append({'local_number':a['local_photo_number'], 
				'ktp': a['local_ktp'],
				'pregnancy_number':a['local_pregnancy_number'],
				'global_number':p.photo_number})
			print 'saving photo', p.pregnancy.patient.ktp, p.pregnancy.pregnancy_number, p.photo_number
		except (Pregnancy.DoesNotExist, Officer.DoesNotExist):
			print 'Pregnancy, photo, Officer not exist'

	#Condition: Add if only if clinic and patient exist, no existing serve, the server_id may vary
	for a in data['add']['serve']:
		try:
			temp = Serve.objects.get(clinic__clinic_id=a['local_clinic_id'], patient__ktp=a['local_ktp'])
		except Serve.DoesNotExist:
			try:
				c = Clinic.objects.get(clinic_id=a['local_clinic_id'])
				p = Patient.objects.get(ktp=a['local_ktp'])
				s = Serve(
					clinic=c,
					patient=p,
					is_active=a['is_active'],
					modify_timestamp=a['modify_timestamp'],
					create_timestamp=a['create_timestamp'],
					server_arrival_timestamp = current_timestamp,
					server_modify_timestamp = current_timestamp,)
				s.save()
				print 'saving serve', p.ktp, c.clinic_id
			except (Clinic.DoesNotExist, Patient.DoesNotExist) as e:		
				print 'Clinic, Patient not exist'

	#Condition: Add if only if clinic and doctor exist, no existing works0n
	print data['add']['works_on']
	for a in data['add']['works_on']:
		try:
			temp = Works_On.objects.get(clinic__clinic_id=a['local_clinic_id'], doctor__user__ktp=a['local_ktp'])
		except Works_On.DoesNotExist:
			try:
				c = Clinic.objects.get(clinic_id=a['local_clinic_id'])
				d = Doctor.objects.get(user__ktp=a['local_ktp'])
				w = Works_On(
					clinic=c,
					doctor=d,
					is_active=a['is_active'],
					modify_timestamp=a['modify_timestamp'],
					create_timestamp=a['create_timestamp'],
					server_arrival_timestamp = current_timestamp,
					server_modify_timestamp = current_timestamp,)
				w.save()
				print 'saving works_on', d.user.ktp, c.clinic_id
			except (Clinic.DoesNotExist, Doctor.DoesNotExist) as e:
				print 'Clinic, Doctor not exist'
	#Condition: Add if only if photo and doctor exist, no existing Validation
	for a in data['add']['validation']:
		try:
			current_photo_number = a['photo_number']
			if  current_photo_number == -1:
				for ii in photo_confirmation:
					if ii['local_number'] == a['local_photo_number'] and ii['ktp'] == a['local_patient_ktp'] and ii['pregnancy_number'] == a['local_pregnancy_number']:
						current_photo_number = ii['global_number']
						break;
			if current_photo_number == -1:
				continue
			temp = Validation.objects.get(doctor__user__ktp=a['local_doctor_ktp'],
				photo__photo_number = current_photo_number,
				photo__pregnancy__pregnancy_number = a['local_pregnancy_number'],
				photo__pregnancy__patient__ktp = a['local_patient_ktp'])
		except Validation.DoesNotExist:
			try:
				if current_photo_number != -1:
					p = Photo.objects.get(photo_number = current_photo_number,
						pregnancy__pregnancy_number = a['local_pregnancy_number'],
						pregnancy__patient__ktp = a['local_patient_ktp'])
					d = Doctor.objects.get(user__ktp=a['local_doctor_ktp'])
					v = Validation(
						doctor=d,
						photo=p,
						x=a['x'],
						y=a['y'],
						a=a['a'],
						b=a['b'],
						tetha=a['tetha'],
						has_seen=a['has_seen'],
						is_active=a['is_active'],
						modify_timestamp=a['modify_timestamp'],
						create_timestamp=a['create_timestamp'],
						server_arrival_timestamp = current_timestamp,
						server_modify_timestamp = current_timestamp,)
					v.save()
					print 'saving validation', d.user.ktp, p.pregnancy.patient.ktp, p.pregnancy.pregnancy_number, p.photo_number
			except (Photo.DoesNotExist, Doctor.DoesNotExist) as e:
				print 'Photo, Doctor not exist'
	comment_confirmation = []
	#Condition: Add as long as KTP + Pregnancy exist. Global photo number may be differ
	for a in data['add']['comment']:
		try:
			d = Doctor.objects.get(user__ktp=a['local_doctor_ktp'])
			o = Officer.objects.get(user__ktp=a['local_officer_ktp'])
			p = Patient.objects.get(ktp=a['local_patient_ktp'])
			last_objects= Comment.objects.filter(patient__ktp=p.ktp).aggregate(Max('comment_number'))
			last_number = last_objects['comment_number__max']
			if  last_number is None:
				last_number = 1
			c = Comment(
				doctor=d,
				officer=o,
				patient=p,
				comment_number=last_number+1,
				from_doctor=a['from_doctor'],
				content=a['content'],
				has_seen=a['has_seen'],
				is_active=a['is_active'],
				modify_timestamp=a['modify_timestamp'],
				create_timestamp=a['create_timestamp'],
				server_arrival_timestamp = current_timestamp,
				server_modify_timestamp = current_timestamp,)
			c.save()
			comment_confirmation.append({'local_number':a['local_comment_number'], 
				'ktp':a['local_patient_ktp'],
				'global_number':c.comment_number})
			print 'saving comment', p.ktp, c.comment_number
		except (Doctor.DoesNotExist, Officer.DoesNotExist, Patient.DoesNotExist):
			print 'Doctor, officer, patient not exist'
			
	#update user, exceptional: username, server_create_timestamp
	for a in data['update']['user']:
		try:
			temp = User.objects.get(ktp=a['ktp'])
			temp.password = a['password']
			temp.name = a['name']
			temp.address = a['address']
			temp.email = a['email']
			temp.phone = a['phone']
			temp.description = a['description']
			temp.is_active = a['is_active']
			temp.modify_timestamp = a['modify_timestamp']
			temp.create_timestamp = a['create_timestamp']
			temp.server_modify_timestamp = current_timestamp
			temp.save()
			print 'user updated', a['ktp']
		except User.DoesNotExist:
			print 'user not exist', a['ktp']
			
	#update patient, exceptional: ktp, server_create_timestamp
	for a in data['update']['patient']:
		try:
			temp = Patient.objects.get(ktp=a['ktp'])
			name=a['name'],
			temp.address=a['address'],
			temp.phone=a['phone'],
			temp.birthdate=a['birthdate'],
			temp.description=a['description'],
			temp.is_active = a['is_active']
			temp.modify_timestamp = a['modify_timestamp']
			temp.create_timestamp = a['create_timestamp']
			temp.server_modify_timestamp = current_timestamp
			temp.save()
			print 'patient updated', a['ktp']
		except Patient.DoesNotExist:
			print 'patient not exist', a['ktp']
	
	#Update pregnancy, except patient pregnancy_number server_create_timestamp
	for a in data['update']['pregnancy']:
		try:
			temp = Pregnancy.objects.get(patient__ktp=a['patient_id'], pregnancy_number=a['pregnancy_number'])
			temp.is_finish=a['is_finish']
			temp.is_active=a['is_active']
			temp.modify_timestamp=a['modify_timestamp']
			temp.create_timestamp=a['create_timestamp']
			temp.server_modify_timestamp = current_timestamp
			temp.save()
			print 'pregnancy updated', a['patient_id'], a['pregnancy_number']
		except Pregnancy.DoesNotExist:
			print 'pregnancy not exist', a['patient_id'], a['pregnancy_number']
			
	#Update doctor, except user_ktp doctor_id server_arrival_timestamp
	for a in data['update']['doctor']:
		try:
			temp = Doctor.objects.get(user__ktp=a['ktp'])
			temp.is_active=a['is_active']
			temp.modify_timestamp=a['modify_timestamp']
			temp.create_timestamp=a['create_timestamp']
			temp.server_modify_timestamp = current_timestamp
			temp.save()
			print 'doctor updated ', a['ktp']
		except Doctor.DoesNotExist:
			print 'doctor not exist', a['ktp']
	
	#Update clinic, except clinic_id server_arrival_timestamp
	for a in data['update']['clinic']:
		try:
			temp = Clinic.objects.get(clinic_id=a['clinic_id'])
			temp.name=a['name']
			temp.address=a['address']
			temp.city=a['city']
			temp.province=a['province']
			temp.phone=a['phone']
			temp.description=a['description']
			temp.is_active=a['is_active']
			temp.modify_timestamp=a['modify_timestamp']
			temp.create_timestamp=a['create_timestamp']
			temp.server_modify_timestamp = current_timestamp
			temp.save()
			print 'clinic updated ', a['clinic_id']
		except Clinic.DoesNotExist:
			print 'clinic not exist', a['clinic_id']
			
	#Update officer, except user_ktp officer_id clinic_id server_arrival_timestamp
	for a in data['update']['officer']:
		try:
			temp = Officer.objects.get(user__ktp=a['ktp'])
			temp.is_active=a['is_active']
			temp.modify_timestamp=a['modify_timestamp']
			temp.create_timestamp=a['create_timestamp']
			temp.server_modify_timestamp = current_timestamp
			temp.save()
			print 'officer updated ', a['ktp']
		except Officer.DoesNotExist:
			print 'officer not exist', a['ktp']
	
	#Update Photo, except  patient_ktp, pregnancy_number, photo_number, officer_ktp server_arrival_timestamp
	for a in data['update']['photo']:
		try:
			temp = Photo.objects.get(pregnancy__patient__ktp=a['ktp'], pregnancy__pregnancy_number=a['pregnancy_number'], photo_number=a['photo_number'])
			temp.analyze_timestamp=a['analyze_timestamp']
			temp.filename=a['filename']
			temp.x=a['x']
			temp.y=a['y']
			temp.a=a['a']
			temp.b=a['b']
			temp.tetha=a['tetha']
			temp.scale=a['scale']
			temp.method=a['method']
			temp.is_active=a['is_active']
			temp.modify_timestamp=a['modify_timestamp']
			temp.create_timestamp=a['create_timestamp']
			temp.server_modify_timestamp = current_timestamp
			temp.save()
			print 'Photo updated ', a['ktp'],a['pregnancy_number'], a['photo_number']
		except Photo.DoesNotExist:
			print 'Photo not exist ', a['ktp'],a['pregnancy_number'], a['photo_number']
	
	#Update Serve, except  clinic_id patient_ktp server_arrival_timestamp
	for a in data['update']['serve']:
		try:
			temp = Serve.objects.get(clinic__clinic_id=a['clinic_id'], patient__ktp=a['ktp'])
			temp.is_active=a['is_active']
			temp.modify_timestamp=a['modify_timestamp']
			temp.create_timestamp=a['create_timestamp']
			temp.server_modify_timestamp = current_timestamp
			temp.save()
			print 'Serve updated ', a['clinic_id'],a['ktp']
		except Serve.DoesNotExist:
			print 'Serve not exist ', a['clinic_id'],a['ktp']
	
	#Update WorksOn, except  clinic_id doctor_ktp server_arrival_timestamp
	for a in data['update']['works_on']:
		try:
			temp = Works_On.objects.get(clinic__clinic_id=a['clinic_id'], doctor__user__ktp=a['ktp'])
			temp.is_active=a['is_active']
			temp.modify_timestamp=a['modify_timestamp']
			temp.create_timestamp=a['create_timestamp']
			temp.server_modify_timestamp = current_timestamp
			temp.save()
			print 'WorksOn updated ', a['clinic_id'],a['ktp']
		except Works_On.DoesNotExist:
			print 'WorksOn not exist ', a['clinic_id'],a['ktp']
			
	#Update Validation, except  photo_number, pregnancy_number, patient_ktp server_arrival_timestamp
	for a in data['update']['validation']:
		try:
			temp = Validation.objects.get(doctor__user__ktp=a['doctor_ktp'],
				photo__photo_number = a['photo_number'],
				photo__pregnancy__pregnancy_number = a['pregnancy_number'],
				photo__pregnancy__patient__ktp = a['patient_ktp'])
			temp.x=a['x']
			temp.y=a['y']
			temp.a=a['a']
			temp.b=a['b']
			temp.tetha=a['tetha']
			temp.has_seen=a['has_seen']
			temp.is_active=a['is_active']
			temp.modify_timestamp=a['modify_timestamp']
			temp.create_timestamp=a['create_timestamp']
			temp.server_modify_timestamp = current_timestamp
			temp.save()
			print 'Validation updated ', a['doctor_ktp'], a['photo_number'], a['pregnancy_number'], a['patient_ktp']
		except Validation.DoesNotExist:
			print 'Validation not exist ', a['doctor_ktp'], a['photo_number'], a['pregnancy_number'], a['patient_ktp']
	
	#Update Validation, except  officer doctor comment_number patient_ktp server_arrival_timestamp
	for a in data['update']['comment']:
		try:
			temp =Comment.objects.get(patient__ktp=a['patient_ktp'],
				comment_number = a['comment_number'])
			temp.from_doctor=a['from_doctor']
			temp.content=a['content']
			temp.has_seen=a['has_seen']
			temp.temp.is_active=a['is_active']
			temp.modify_timestamp=a['modify_timestamp']
			temp.create_timestamp=a['create_timestamp']
			temp.server_modify_timestamp = current_timestamp
			temp.save()
			print 'Validation updated ', a['patient_ktp'], a['comment_number']
		except Comment.DoesNotExist:
			print 'Validation updated ', a['patient_ktp'], a['comment_number']
	
	# confirm_doctor = []
	# confirm_json = {'user':confirm_user,
		# 'doctor':confirm_doctor}
	
	###Cari new Addition
	
	#table user
	new_user_json = [];
	new_users = User.objects.all().filter(server_arrival_timestamp__gt = timestamp, is_active = True);
	for user in new_users:
		new_user_json.append(user.get_json());
	
	#table doctor
	new_doctor_json = []
	new_doctors = Doctor.objects.all().filter(server_arrival_timestamp__gt = timestamp, is_active = True)
	for doctor in new_doctors:
		new_doctor_json.append(doctor.get_json())
		
	#table clinic
	new_clinic_json = []
	new_clinics = Clinic.objects.all().filter(server_arrival_timestamp__gt = timestamp, is_active = True)
	for clinic in new_clinics:
		new_clinic_json.append(clinic.get_json())
		
	#table officer
	new_officer_json = []
	new_officers = Officer.objects.all().filter(server_arrival_timestamp__gt = timestamp, is_active = True)
	for officer in new_officers:
		new_officer_json.append(officer.get_json())
		
	#table patient
	new_patient_json = []
	new_patients = Patient.objects.all().filter(server_arrival_timestamp__gt = timestamp, is_active = True)
	for patient in new_patients:
		new_patient_json.append(patient.get_json())
		
	#table pregnancy
	new_pregnancy_json = []
	new_pregnancies = Clinic.objects.all().filter(server_arrival_timestamp__gt = timestamp, is_active = True)
	for pregnancy in new_pregnancies:
		new_pregnancy_json.append(pregnancy.get_json())
	
	#table photo
	new_photo_json = []
	new_photos = Photo.objects.all().filter(server_arrival_timestamp__gt = timestamp, is_active = True)
	for photo in new_photos:
		new_photo_json.append(photo.get_json())
		
	#table serve
	new_serve_json = []
	new_serves = Serve.objects.all().filter(server_arrival_timestamp__gt = timestamp, is_active = True)
	for serve in new_serves:
		new_serve_json.append(serve.get_json())
		
	#table works_on
	new_workson_json = []
	new_worksons = Works_On.objects.all().filter(server_arrival_timestamp__gt = timestamp, is_active = True)
	for workson in new_worksons:
		new_workson_json.append(workson.get_json())
		
	#table validation
	new_validation_json = []
	new_validations = Validation.objects.all().filter(server_arrival_timestamp__gt = timestamp, is_active = True)
	for validation in new_validations:
		new_validation_json.append(validation.get_json())
	
	#table comment
	new_comment_json = []
	new_comments = Comment.objects.all().filter(server_arrival_timestamp__gt = timestamp, is_active = True)
	for comment in new_comments:
		new_comment_json.append(comment.get_json())
		
	#table user
	update_user_json = [];
	update_users = User.objects.all().filter(Q(is_active = True) & Q(server_modify_timestamp__gt = timestamp) | Q(modify_timestamp__gt = timestamp))
	for user in update_users:
		update_user_json.append(user.get_json());
	
	#table doctor
	update_doctor_json = []
	update_doctors = Doctor.objects.all().filter(Q(is_active = True) & Q(server_modify_timestamp__gt = timestamp) | Q(modify_timestamp__gt = timestamp))
	for doctor in update_doctors:
		update_doctor_json.append(doctor.get_json())
		
	#table clinic
	update_clinic_json = []
	update_clinics = Clinic.objects.all().filter(Q(is_active = True) & Q(server_modify_timestamp__gt = timestamp) | Q(modify_timestamp__gt = timestamp))
	for clinic in update_clinics:
		update_clinic_json.append(clinic.get_json())
		
	#table officer
	update_officer_json = []
	update_officers = Officer.objects.all().filter(Q(is_active = True) & Q(server_modify_timestamp__gt = timestamp) | Q(modify_timestamp__gt = timestamp))
	for officer in update_officers:
		update_officer_json.append(officer.get_json())
		
	#table patient
	update_patient_json = []
	update_patients = Patient.objects.all().filter(Q(is_active = True) & Q(server_modify_timestamp__gt = timestamp) | Q(modify_timestamp__gt = timestamp))
	for patient in update_patients:
		update_patient_json.append(patient.get_json())
		
	#table pregnancy
	update_pregnancy_json = []
	update_pregnancies = Clinic.objects.all().filter(Q(is_active = True) & Q(server_modify_timestamp__gt = timestamp) | Q(modify_timestamp__gt = timestamp))
	for pregnancy in update_pregnancies:
		update_pregnancy_json.append(pregnancy.get_json())
	
	#table photo
	update_photo_json = []
	update_photos = Photo.objects.all().filter(Q(is_active = True) & Q(server_modify_timestamp__gt = timestamp) | Q(modify_timestamp__gt = timestamp))
	for photo in update_photos:
		update_photo_json.append(photo.get_json())
		
	#table serve
	update_serve_json = []
	update_serves = Serve.objects.all().filter(Q(is_active = True) & Q(server_modify_timestamp__gt = timestamp) | Q(modify_timestamp__gt = timestamp))
	for serve in update_serves:
		update_serve_json.append(serve.get_json())
		
	#table works_on
	update_workson_json = []
	update_worksons = Works_On.objects.all().filter(Q(is_active = True) & Q(server_modify_timestamp__gt = timestamp) | Q(modify_timestamp__gt = timestamp))
	for workson in update_worksons:
		update_workson_json.append(workson.get_json())
		
	#table validation
	update_validation_json = []
	update_validations = Validation.objects.all().filter(Q(is_active = True) & Q(server_modify_timestamp__gt = timestamp) | Q(modify_timestamp__gt = timestamp))
	for validation in update_validations:
		update_validation_json.append(validation.get_json())
	
	#table comment
	update_comment_json = []
	update_comments = Comment.objects.all().filter(Q(is_active = True) & Q(server_modify_timestamp__gt = timestamp) | Q(modify_timestamp__gt = timestamp))
	for comment in update_comments:
		update_comment_json.append(comment.get_json())
	
	return HttpResponse(simplejson.dumps(
		{
			'add': {'user':new_user_json, 
					'doctor': new_doctor_json,
					'clinic': new_clinic_json,
					'officer': new_officer_json,
					'patient': new_patient_json,
					'pregnancy': new_pregnancy_json,
					'photo': new_photo_json,
					'serve': new_serve_json,
					'works_on': new_workson_json,
					'validation': new_validation_json,
					'comment': new_comment_json,},
			'update': {'user':update_user_json, 
					'doctor': update_doctor_json,
					'clinic': update_clinic_json,
					'officer': update_officer_json,
					'patient': update_patient_json,
					'pregnancy': update_pregnancy_json,
					'photo': update_photo_json,
					'serve': update_serve_json,
					'works_on': update_workson_json,
					'validation': update_validation_json,
					'comment': update_comment_json,},
			'confirm_add': {'photo' : photo_confirmation,
					'comment': comment_confirmation,},
		},indent=4), mimetype="application/json")