from django.db import models
from django.utils import timezone
import datetime
 
class User(models.Model):
	ktp = models.CharField(max_length=20, primary_key=True)
	username = models.CharField(max_length=30, blank=False, unique=True)
	password = models.CharField(max_length=30, blank=False)
	name = models.CharField(max_length=30, null=False)
	address = models.CharField(max_length=50, blank=True)
	email = models.CharField(max_length=75, blank=True)
	phone = models.CharField(max_length=30, blank=True)
	description = models.TextField(blank=True)
	is_active = models.BooleanField(default=True)
	modify_timestamp = models.BigIntegerField(null=False)
	create_timestamp = models.BigIntegerField(null=False)
	server_arrival_timestamp = models.BigIntegerField(null=False)
	server_modify_timestamp = models.BigIntegerField(null=False)
	def __unicode__(self):
		return self.ktp + ' - ' + self.username
	def get_json(self):
		a = {'ktp':self.ktp,
			'username':self.username,
			'password':self.password,
			'name':self.name,
			'address':self.address,
			'email':self.email,
			'phone':self.phone,
			'description':self.description,
			'is_active':self.is_active,
			'modify_timestamp':self.modify_timestamp,
			'create_timestamp':self.create_timestamp,}
		return a
		
		
class Patient(models.Model):
	ktp = models.CharField(max_length=20, primary_key=True)
	name = models.CharField(max_length=30, blank=False)
	address = models.CharField(max_length=50, blank=True)
	phone = models.CharField(max_length=30, blank=True)
	birthdate = models.BigIntegerField(null=False)
	filename = models.CharField(max_length=30, blank=True)
	description = models.TextField(blank=True)
	is_active = models.BooleanField(default=True)
	modify_timestamp = models.BigIntegerField(null=False)
	create_timestamp = models.BigIntegerField(null=False)
	server_arrival_timestamp = models.BigIntegerField(null=False)
	server_modify_timestamp = models.BigIntegerField(null=False)
	def __unicode__(self):
		return self.ktp + ' - ' + self.name
	def get_json(self):
		a = {
			'ktp':self.ktp,
			'name':self.name,
			'address':self.address,
			'phone':self.phone,
			'birthdate':self.birthdate,
			'filename':self.filename,
			'description':self.description,
			'is_active ':self.is_active ,
			'modify_timestamp ':self.modify_timestamp ,
			'create_timestamp ':self.create_timestamp ,}
		return a;


class Pregnancy(models.Model):
	pregnancy_id = models.AutoField(primary_key=True)
	patient = models.ForeignKey(Patient, blank=False)
	pregnancy_number = models.IntegerField(null=False)
	is_finish = models.BooleanField(null=False)
	is_active = models.BooleanField(default=True)
	modify_timestamp = models.BigIntegerField(null=False)
	create_timestamp = models.BigIntegerField(null=False)
	server_arrival_timestamp = models.BigIntegerField(null=False)
	server_modify_timestamp = models.BigIntegerField(null=False)
	def __unicode__(self):
		return str(self.pregnancy_id) + ' - ' + self.patient.ktp + ' - preg ' + str(self.pregnancy_number)
	def validate_unique(self, *args, **kwargs):
		super(Pregnancy, self).validate_unique(*args, **kwargs)
		qs = self.__class__.objects.filter(
			patient__ktp=self.patient.ktp,
			pregnancy_number=self.pregnancy_number,
		)
		if qs.exists():
			raise ValidationError('Violating Unique constraint of Pregnancy(patient, pregnancy_number)')
	def get_json(self):
		a = {
			'pregnancy_id':self.pregnancy_id,
			'patient_id':self.patient.ktp,
			'pregnancy_number':self.pregnancy_number,
			'is_finish':self.is_finish,
			'is_active':self.is_active,
			'modify_timestamp':self.modify_timestamp,
			'create_timestamp':self.create_timestamp,}
		return a
			
class Photo(models.Model):
	photo_id = models.AutoField(primary_key=True)
	pregnancy = models.ForeignKey(Pregnancy, null=False)
	photo_number = models.IntegerField(null=False)
	officer = models.ForeignKey('Officer', blank=False)
	analyze_timestamp = models.BigIntegerField(null=True)
	filename = models.CharField(max_length=50, blank=False)
	x = models.DecimalField(max_digits=10, decimal_places=5, null=True)
	y = models.DecimalField(max_digits=10, decimal_places=5, null=True)
	a = models.DecimalField(max_digits=10, decimal_places=5, null=True)
	b = models.DecimalField(max_digits=10, decimal_places=5, null=True)
	tetha = models.DecimalField(max_digits=10, decimal_places=5, null=True)
	scale = models.DecimalField(max_digits=10, decimal_places=5, null=True)
	method = models.CharField(max_length=30, blank=True)
	is_active = models.BooleanField(default=True)
	modify_timestamp = models.BigIntegerField(null=False)
	create_timestamp = models.BigIntegerField(null=False)
	server_arrival_timestamp = models.BigIntegerField(null=False)
	server_modify_timestamp = models.BigIntegerField(null=False)
	def __unicode__(self):
		return str(self.photo_id) + ' - ' + self.pregnancy.patient.ktp + ' - preg ' + str(self.pregnancy.pregnancy_number) + ' - no '+ str(self.photo_number)
	def validate_unique(self, *args, **kwargs):
		super(Photo, self).validate_unique(*args, **kwargs)
		qs = self.__class__.objects.filter(
			pregnancy__pregnancy_id=self.pregnancy.pregnancy_id,
			photo_number=self.photo_number,
		)
		if qs.exists():
			raise ValidationError('Violating Unique constraint of Photo(pregnancy, photo_number)')
	def get_json(self):
		a = {
			'photo_id':self.photo_id,
			'pregnancy_id':self.pregnancy.pregnancy_id,
			'ktp': self.pregnancy.patient.ktp,
			'pregnancy_number':self.pregnancy.pregnancy_number,
			'photo_number':self.photo_number,
			'officer_ktp' : self.officer.user.ktp,
			'analyze_timestamp':self.analyze_timestamp,
			'filename':self.filename,
			'x':float(self.x),
			'y':float(self.y),
			'a':float(self.a),
			'b':float(self.b),
			'tetha':float(self.tetha),
			'scale':float(self.scale),
			'method':self.method,
			'is_active':self.is_active,
			'modify_timestamp':self.modify_timestamp,
			'create_timestamp':self.create_timestamp,}
		return a
	
class Doctor(models.Model):
	user = models.ForeignKey(User, primary_key=True)
	doctor_id = models.IntegerField(unique=True, null=False)
	is_active = models.BooleanField(default=True)
	photos = models.ManyToManyField(Photo, through='Validation')
	modify_timestamp = models.BigIntegerField(null=False)
	create_timestamp = models.BigIntegerField(null=False)
	server_arrival_timestamp = models.BigIntegerField(null=False)
	server_modify_timestamp = models.BigIntegerField(null=False)
	def __unicode__(self):
		return self.user.ktp + ' - ' + str(self.doctor_id)
	def get_json(self):
		a = {
			'ktp':self.user.ktp,
			'doctor_id':self.doctor_id,
			'is_active':self.is_active,
			'modify_timestamp':self.modify_timestamp,
			'create_timestamp':self.create_timestamp,}
		return a
		
class Clinic(models.Model):
	clinic_id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=30, blank=False)
	address = models.CharField(max_length=50, blank=True)
	city = models.CharField(max_length=30, blank=True)
	province = models.CharField(max_length=30, blank=True)
	phone = models.CharField(max_length=30, blank=True)
	description = models.TextField(blank=True)
	patients = models.ManyToManyField(Patient, through='Serve')
	doctors = models.ManyToManyField(Doctor, through='Works_On')
	is_active = models.BooleanField(default=True)
	modify_timestamp = models.BigIntegerField(null=False)
	create_timestamp = models.BigIntegerField(null=False)
	server_arrival_timestamp = models.BigIntegerField(null=False)
	server_modify_timestamp = models.BigIntegerField(null=False)
	def __unicode__(self):
		return str(self.clinic_id) + ' - ' +self.name
	def get_json(self):
		a = {
			'clinic_id':self.clinic_id,
			'name':self.name,
			'address':self.address,
			'city':self.city,
			'province':self.province,
			'phone':self.phone,
			'description':self.description,
			'is_active':self.is_active,
			'modify_timestamp':self.modify_timestamp,
			'create_timestamp':self.create_timestamp,}
		return a
		
class Officer(models.Model):
	user = models.ForeignKey(User, primary_key=True)
	officer_id = models.IntegerField(unique=True, null=False)
	clinic = models.ForeignKey(Clinic, null=True)
	is_active = models.BooleanField(default=True)
	modify_timestamp = models.BigIntegerField(null=False)
	create_timestamp = models.BigIntegerField(null=False)
	server_arrival_timestamp = models.BigIntegerField(null=False)
	server_modify_timestamp = models.BigIntegerField(null=False)
	def __unicode__(self):
		return self.user.ktp + ' - ' + str(self.officer_id)
	def get_json(self):
		a = {
			'ktp':self.user.ktp,
			'officer_id':self.officer_id,
			'clinic_id':self.clinic.clinic_id,
			'is_active':self.is_active,
			'modify_timestamp':self.modify_timestamp,
			'create_timestamp':self.create_timestamp,}
		return a
			
class Serve(models.Model):
	serve_id = models.AutoField(primary_key=True)
	clinic = models.ForeignKey(Clinic)
	patient = models.ForeignKey(Patient)
	is_active = models.BooleanField(default=True)
	modify_timestamp = models.BigIntegerField(null=False)
	create_timestamp = models.BigIntegerField(null=False)
	server_arrival_timestamp = models.BigIntegerField(null=False)
	server_modify_timestamp = models.BigIntegerField(null=False)
	def __unicode__(self):
		return str(self.serve_id) + ' - ' + str(self.clinic.clinic_id) + ' - ' + self.patient.ktp
	def validate_unique(self, *args, **kwargs):
		super(Serve, self).validate_unique(*args, **kwargs)
		qs = self.__class__.objects.filter(
			patient__ktp=self.patient.ktp,
			clinic__clinic_id=self.clinic.clinic_id,
		)
		if qs.exists():
			raise ValidationError('Violating Unique constraint Serve(clinic, patient)')
	def get_json(self):
		a = {
			'serve_id':self.serve_id,
			'clinic_id':self.clinic.clinic_id,
			'ktp':self.patient.ktp,
			'is_active':self.is_active,
			'modify_timestamp':self.modify_timestamp,
			'create_timestamp':self.create_timestamp,}
		return a
	
class Works_On(models.Model):
	works_id = models.AutoField(primary_key=True)
	doctor = models.ForeignKey(Doctor, blank=False)
	clinic = models.ForeignKey(Clinic, null=False)
	is_active = models.BooleanField(default=True)
	modify_timestamp = models.BigIntegerField(null=False)
	create_timestamp = models.BigIntegerField(null=False)
	server_arrival_timestamp = models.BigIntegerField(null=False)
	server_modify_timestamp = models.BigIntegerField(null=False)
	def __unicode__(self):
		return str(self.works_id) + ' - doctor ' + self.doctor.user.ktp + ' - clinic ' + str(self.clinic.clinic_id)
	def validate_unique(self, *args, **kwargs):
		super(Works_On, self).validate_unique(*args, **kwargs)
		qs = self.__class__.objects.filter(
			doctor__user__ktp=self.doctor.user.ktp,
			clinic__clinic_id=self.clinic.clinic_id,
		)
		if qs.exists():
			raise ValidationError('Violating Unique constraint Works_on(clinic, doctor)')
	def get_json(self):
		a = {
			'works_id':self.works_id,
			'ktp':self.doctor.user.ktp,
			'clinic_id':self.clinic.clinic_id,
			'is_active':self.is_active,
			'modify_timestamp':self.modify_timestamp,
			'create_timestamp':self.create_timestamp,}
		return a
		
class Validation(models.Model):
	validation_id = models.AutoField(primary_key=True)
	doctor = models.ForeignKey(Doctor, blank=False)
	photo = models.ForeignKey(Photo, null=False)
	x = models.DecimalField(max_digits=10, decimal_places=5, null=True)
	y = models.DecimalField(max_digits=10, decimal_places=5, null=True)
	a = models.DecimalField(max_digits=10, decimal_places=5, null=True)
	b = models.DecimalField(max_digits=10, decimal_places=5, null=True)
	tetha = models.DecimalField(max_digits=10, decimal_places=5, null=True)
	has_seen = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	modify_timestamp = models.BigIntegerField(null=False)
	create_timestamp = models.BigIntegerField(null=False)
	server_arrival_timestamp = models.BigIntegerField(null=False)
	server_modify_timestamp = models.BigIntegerField(null=False)
	def __unicode__(self):
		return str(self.validation_id) + ' - doctor' + self.doctor.user.ktp + ' - photo ' + str(self.photo.photo_id)
	def validate_unique(self, *args, **kwargs):
		super(Validation, self).validate_unique(*args, **kwargs)
		qs = self.__class__.objects.filter(
			doctor__user__ktp=self.doctor.user.ktp,
			photo__photo_id=self.photo.photo_id,
		)
		if qs.exists():
			raise ValidationError('Violating Unique constraint Validation(doctor, photo)')
	def get_json(self):
		a = {
			'validation_id':self.validation_id,
			'doctor_ktp':self.doctor.user.ktp,
			'photo_number':self.photo.photo_number,
			'patient_ktp':self.photo.pregnancy.patient.ktp,
			'pregnancy_number':self.photo.pregnancy.pregnancy_number,
			'photo_number':self.photo.photo_number,
			'x':float(self.x),
			'y':float(self.y),
			'a':float(self.a),
			'b':float(self.b),
			'tetha':float(self.tetha),
			'has_seen':self.has_seen,
			'is_active':self.is_active,
			'modify_timestamp':self.modify_timestamp,
			'create_timestamp':self.create_timestamp,}
		return a		
			
class Comment(models.Model):
	comment_id = models.AutoField(primary_key=True)
	doctor = models.ForeignKey(Doctor, blank=True)
	officer = models.ForeignKey(Officer, blank=True)
	patient = models.ForeignKey(Patient, blank=False)
	comment_number = models.IntegerField(null=False)
	from_doctor = models.BooleanField(null=False)
	content = models.TextField(blank=False)
	has_seen = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	modify_timestamp = models.BigIntegerField(null=False)
	create_timestamp = models.BigIntegerField(null=False)
	server_arrival_timestamp = models.BigIntegerField(null=False)
	server_modify_timestamp = models.BigIntegerField(null=False)
	def __unicode__(self):
		return str(self.comment_id) + ' - user ' + self.patient.ktp + ' - ' + str(self.comment_number)
	def validate_unique(self, *args, **kwargs):
		super(Comment, self).validate_unique(*args, **kwargs)
		qs = self.__class__.objects.filter(
			patient__ktp=self.patient.ktp,
			comment_number=self.comment_number,
		)
		if qs.exists():
			raise ValidationError('Violating Unique constraint Comment(patient, comment_number)')
	def get_json(self):
		a = {
			'comment_id':self.comment_id,
			'doctor_ktp':self.doctor.user.ktp,
			'officer_ktp':self.officer.user.ktp,
			'patient_ktp':self.patient.ktp,
			'comment_number':self.comment_number,
			'from_doctor':self.from_doctor,
			'content':self.content,
			'has_seen':self.has_seen,
			'is_active':self.is_active,
			'modify_timestamp':self.modify_timestamp,
			'create_timestamp':self.create_timestamp,}
		return a