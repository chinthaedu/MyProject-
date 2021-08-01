from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from App.models import Songs,Movie
from App.forms import SongsForm,MoviesForm,UsgForm,Rltype,Rlupd,Pfupd,Chgepwd
from App.models import Rolereq,User
#EMAIL concept
from PlayMusic import settings
from django.core.mail import send_mail
import random
    


# Create your views here.

def home(request):
	alldata=Movie.objects.all()
	allsongs=list(Songs.objects.all())
	print(allsongs)
	recent=Songs.objects.all().first()
	top6=random.sample(allsongs,6)
	carData={}
	for s in top6:
		for m in alldata:
			if s.mv_id==m.id:
				carData[s.id]=s.id,m.id,s.songname,s.song.url,m.moviename,m.album.url
	if list(Movie.objects.all())!=[]:
		rcmovie=Movie.objects.get(id=recent.mv_id)
	else:
		return render(request,'ht1/home.html',{'alldata':alldata,'top6':top6})
	return render(request,'ht1/home.html',{'alldata':alldata,'top6':top6,'recent':recent,'rcmovie':rcmovie,'carData':carData.values()})


class SendFav:
	def __init__(self,request):
		t=User.objects.get(id=request.user.id)
		s=Songs.objects.all()
		songsids=[]
		for i in s:
			songsids.append(i.id)

		self.slist=t.fav.split(',')
		for i in self.slist:
			if i=='':
				self.slist.remove('')
		for i in self.slist:
			if int(i) not in songsids:
				self.slist.remove(i)

		self.favsongs=[]
		self.mov=[]
		for i in self.slist:
			song=Songs.objects.get(id=i)
			self.favsongs.append(song)
			self.mov.append(Movie.objects.get(id=song.mv_id))
		# if self.slist!=[]:
		# 	self.favsongs=[]
		# 	self.mov=[]
		# 	for i in self.slist:
		# 		song=Songs.objects.get(id=i)
		# 		self.favsongs.append(song)
		# 		self.mov.append(Movie.objects.get(id=song.mv_id))

		t.fav=','.join(self.slist)
		t.save()
	
		self.data={}
		for i in range(len(self.favsongs)):
			self.data[i]=self.favsongs[i].songname,self.favsongs[i].song.url,self.mov[i].album.url,self.favsongs[i].id,self.mov[i].id
		
	def getfav(self):
		return self.favsongs

	def getmovie(self):
		return self.mov

	def getFavData(self):
		return self.data


class SendRec:
	def __init__(self,request):
		r=User.objects.get(id=request.user.id)
		s=Songs.objects.all()
		songsids=[]
		for i in s:
			songsids.append(i.id)
		self.songslist=r.rec.split(',')
	
		for i in self.songslist:
			if i=='':
				self.songslist.remove('')

		self.newsongslist=[]
		for i in self.songslist:
			if int(i) in songsids:
				self.newsongslist.append(i)

		self.recentsongs=[]
		self.recentmovies=[]
		for i in self.newsongslist:
			song=Songs.objects.get(id=i)
			self.recentsongs.append(song)
			self.recentmovies.append(Movie.objects.get(id=song.mv_id))

		
		r.rec=','.join(self.newsongslist)
		r.save()
		
		self.rdata={}
		for i in range(len(self.recentsongs)):
			self.rdata[i]=self.recentsongs[i].songname,self.recentsongs[i].song.url,self.recentmovies[i].album.url,self.recentsongs[i].id,self.recentmovies[i].id


	def getrecsongs(self):
		return self.recentsongs

	def getrecmovie(self):
		return self.recentmovies

	def getRecData(self):
		return self.rdata


# class SendLikes:
# 	def _init_(self,request):
# 		r=User.objects.get(id=request.user.id)
# 		s=Songs.objects.all()
# 		songsids=[]
# 		for i in s:
# 			songsids.append(i.id)
# 		self.songslist=r.likes.split(',')
	
# 		for i in self.songslist:
# 			if i=='':
# 				self.songslist.remove('')

# 		self.newsongslist=[]
# 		for i in self.songslist:
# 			if int(i) in songsids:
# 				self.newsongslist.append(i)

# 		self.likedsongs=[]
# 		self.likedmovies=[]
# 		for i in self.newsongslist:
# 			song=Songs.objects.get(id=i)
# 			self.likedsongs.append(song)
# 			self.likedmovies.append(Movie.objects.get(id=song.mv_id))

		
# 		r.likes=','.join(self.newsongslist)
# 		r.save()
		
# 		self.rdata={}
# 		for i in range(len(self.likedsongs)):
# 			self.rdata[i]=self.likedsongs[i].songname,self.likedsongs[i].song.url,self.likedmovies[i].album.url,self.likedsongs[i].id,self.likedmovies[i].id


	# def getrecsongs(self):
	# 	return self.likedsongs

	# def getrecmovie(self):
	# 	return self.likedmovies

	# def getRecData(self):
	# 	return self.rdata


def moviesongslist(request,mid):
	mvdetails=Movie.objects.get(id=mid)
	mvsongs=Songs.objects.filter(mv_id=mid)
	obj1=SendFav(request)
	favlist=obj1.getfav()

	favyesno=[]
	for i in mvsongs:
		if i in favlist:
			favyesno.append(1)
		else:
			favyesno.append(0)

	return render(request,'ht1/moviesongslist.html',{'mv':mvdetails,'s':mvsongs,'favlist':favlist,'favyesno':favyesno})

def addsong(request):
	movies=[]
	mv=list(Movie.objects.all())
	for i in mv:
		movies.append(i.moviename)
	row=SongsForm()
	allsongs=Songs.objects.all()
	if request.method=="POST":
		s=SongsForm(request.POST,request.FILES)
		if s.is_valid(): 
			n=s.save(commit=False)   
			n.mv_id=Movie.objects.get(moviename=request.POST['moviename']).id
			messages.success(request,"{} Song added Successfully".format(n.songname))
			n.save()
			n.songno=len(Songs.objects.filter(mv_id=n.mv_id))
			n.save()
		return redirect('/addsong')
	return render(request,'ht1/addsong.html',{'songform':row,'movies':movies,'a':allsongs})


def addMovie(request):
	rowm=MoviesForm()
	data=Movie.objects.all()
	movies=[]
	mvs=Movie.objects.all()
	for i in mvs:
		movies.append(i.moviename)
	if request.method=="POST":
		m=MoviesForm(request.POST,request.FILES)
		if m.is_valid():
			n=m.save(commit=False)  
			if n.moviename in movies:
				messages.error(request,"{} movie already existed".format(n.moviename))
			else:
				messages.success(request,"{} movie added Successfully".format(n.moviename))
				n.save()
		return render(request,'ht1/addMovie.html',{'movieform':rowm,"data":data,"existed":movies})
	return render(request,'ht1/addMovie.html',{'movieform':rowm,"data":data,"existed":movies})



def playsong(request,sid,mid):
	s=Songs.objects.get(id=sid)
	m=Movie.objects.get(id=mid)
	r=User.objects.get(id=request.user.id)
	r.rec+=','+str(sid)
	r.save()
	obj1=SendRec(request)
	# recsongs=obj1.getrecsongs()
	# recmovie=obj1.getrecmovie()
	# rdata=obj1.getRecData()
	obj1=SendFav(request)
	favlist=obj1.getfav()
	corresponding_movie_songs=Songs.objects.filter(mv_id=mid)
	return render(request,'ht1/playingsong.html',{'song':s,'movie':m,'favlist':favlist,'all':corresponding_movie_songs}) 

def nextsong(request,sid,mid):
	alls=Songs.objects.filter(mv_id=mid)
	msongs=[]
	for i in alls:
		msongs.append(i.songno)
	msongs.sort()
	s=Songs.objects.get(id=sid,mv_id=mid)
	m=Movie.objects.get(id=mid)
	ind=msongs.index(s.songno)
	if ind==len(msongs)-1:
		ind=0
	else:
		ind+=1

	n=msongs[ind]
	s=Songs.objects.get(songno=n,mv_id=mid)

	r=User.objects.get(id=request.user.id)
	r.rec+=','+str(sid)
	r.save()
	obj1=SendRec(request)
	recsongs=obj1.getrecsongs()
	recmovie=obj1.getrecmovie()
	rdata=obj1.getRecData()
	obj2=SendFav(request)
	favlist=obj2.getfav()
	return render(request,'ht1/playingsong.html',{'song':s,'movie':m,'favlist':favlist,'all':alls})

def prevsong(request,sid,mid):
	alls=Songs.objects.filter(mv_id=mid)
	msongs=[]
	for i in alls:
		msongs.append(i.songno)
	
	msongs.sort()
	s=Songs.objects.get(id=sid,mv_id=mid)
	m=Movie.objects.get(id=mid)
	ind=msongs.index(s.songno)

	if ind==0:
		ind=len(msongs)-1
	else:
		ind-=1
	n=msongs[ind]
	
	s=Songs.objects.get(songno=n,mv_id=mid)

	r=User.objects.get(id=request.user.id)
	r.rec+=','+str(sid)
	r.save()
	obj1=SendRec(request)
	recsongs=obj1.getrecsongs()
	recmovie=obj1.getrecmovie()
	rdata=obj1.getRecData()

	obj2=SendFav(request)
	favlist=obj2.getfav()

	return render(request,'ht1/playingsong.html',{'song':s,'movie':m,'favlist':favlist,'all':alls})

def moviesList(request,id):
	m=Songs.objects.filter(mv_id=id)
	alb=Movie.objects.get(id=id)
	return render(request,'ht1/SingleMovie.html',{"m":m,"alb":alb})

def updatesong(request,id):
	s=Songs.objects.get(id=id)
	if request.method=="POST":
		e=SongsForm(request.POST,request.FILES,instance=s)
		if e.is_valid():
			e.save()
		return redirect('/addsong')
	e=SongsForm(instance=s)
	return render(request,'ht1/songupdate.html',{"q":e})

def deletesong(request,id):
	s=Songs.objects.get(id=id)
	s.delete()
	return redirect('/addsong')

def usrreg(request):
	if request.method=="POST":
		d=UsgForm(request.POST)
		if d.is_valid():
			d.save()
			return redirect('/login')
	d=UsgForm()
	return render(request,'ht1/userregister.html',{'t':d})



def rolereq(request):
	p=Rolereq.objects.filter(ud_id=request.user.id).count()

	if request.method=="POST":
		k=Rltype(request.POST,request.FILES)
		if k.is_valid():
			y=k.save(commit=False)
			y.ud_id=request.user.id
			y.uname=request.user.username
			y.save()
			return redirect('/')

	k=Rltype()
	return render(request,'ht1/rolereq.html',{'d':k,'c':p})

def gveperm(request):
	u=User.objects.all()
	r=Rolereq.objects.all()
	d={}
	for n in u:
		for m in r:
			if n.is_superuser == 1 or n.id!=m.ud_id:
				continue
			else:
				d[n.id]=m.uname,m.rltype,n.role,n.id
	return render(request,'ht1/givepermissions.html',{'h':d.values()})

def gvupdate(request,t):
	print("USER ID",t)
	y=Rolereq.objects.get(ud_id=t)
	d=User.objects.get(id=t)
	if request.method=="POST":
		n=Rlupd(request.POST,instance=d)
		if n.is_valid():
			n.save()
			y.is_checked=1
			y.save()
		return redirect('/gvper')
	n=Rlupd(instance=d)
	#userrow=User.objects.get(id=row.ud_id)
	#if request.method=="POST":
	#	#row.uname=request.POST['uname']
	#	row.rltype=request.POST['rltype']
	#	userrow.role=request.POST['role']
	#	print(userrow.role)
	#	row.save()
	#	print("YESS")
	#	userrow.save()
	#	print("ALSO")
	#	return gveperm(request)
	#return render(request,'app/gvupdate.html',{'row':row,'u':userrow})
	return render(request,'ht1/gvupdate.html',{"n":n})

def pfle(request):
	userdata=User.objects.get(id=request.user.id)
	#k=Profile(instance=userdata)
	return render(request,'ht1/profile.html',{"u":userdata})


def profileUpdate(request,id):
	userdata=User.objects.get(id=id)
	if request.method=="POST":
		userdata.username=request.POST.get('username')
		userdata.email=request.POST.get('email')
		userdata.mobilenumber=request.POST.get('mobile')
		userdata.age=request.POST.get('age')
		userdata.first_name=request.POST.get('fname')
		userdata.last_name=request.POST.get('lname')

		userdata.save()
		return pfle(request,id=id)
	return render(request,'ht1/profileupdate.html',{"us":userdata})

@login_required
def feedback(request):
	if request.method=="POST":
		sd=request.POST['snmail'].split(',')
		sm=request.POST['sub']
		mg=request.POST['msg']
		rt=settings.EMAIL_HOST_USER
		#sen_mail(sub,msg,sender,receivers)
		dt=send_mail(sm,mg,rt,sd)
		if dt==1:
			messages.success(request,"Feedback sent Successfully")
			return redirect(request.META['HTTP_REFERER'])
		else:
			messages.danger(request,"Feedback failed to sent")
			return redirect(request.META['HTTP_REFERER'])
	return render(request,'ht1/feedback.html')

def pfleupd(request):
	t=User.objects.get(id=request.user.id)
	if request.method=="POST":
		pfle=Pfupd(request.POST,request.FILES,instance=t)
		if pfle.is_valid():
			pfle.save()
			return redirect('/pfle')
	pfle=Pfupd(instance=t) 
	return render(request,'ht1/pfleupdate.html',{'u':pfle})


def changepwd(request):
	if request.method=="POST":
		k=Chgepwd(user=request.user,data=request.POST)
		if k.is_valid():
			k.save()
			print("success")
			return redirect('/login')
		else:
			print("fail")
	k=Chgepwd(user=request)
	return render(request,'ht1/changepwd.html',{'t':k})


def updatemovie(request,id):
	m=Movie.objects.get(id=id)
	if request.method=="POST":
		k=MoviesForm(request.POST,request.FILES,instance=m)
		if k.is_valid():
			n=k.save(commit=False)  
			messages.success(request,"{} movie added Successfully".format(n.moviename))
			n.save()
		return redirect('/addmovie')
	return render(request,'ht1/updatemovie.html',{"data":m})


def deletemovie(request,id):
	m=Movie.objects.get(id=id)
	m.delete()

	return redirect('/addmovie')


def favourites(request):
	obj1=SendFav(request)
	favsongs=obj1.getfav()
	mov=obj1.getmovie()
	data=obj1.getFavData()
	return render(request,'ht1/favourites.html',{'favsongs':favsongs,'mov':mov,'data':data.values()})

def addFavourites(request,sid):
	t=User.objects.get(id=request.user.id)
	t.fav=t.fav+','+str(sid)
	print(t.fav)
	t.save()
	return redirect(request.META['HTTP_REFERER'])
def deleteuser(request,id):
	u=User.objects.get(id=id)
	messages.success(request,"{} deleted Successfully".format(u.username))
	u.delete()
	return redirect(request.META['HTTP_REFERER'])

def removeFavourites(request,sid):
	t=User.objects.get(id=request.user.id)

	obj1=SendFav(request)
	favsongs=obj1.getfav()
	mov=obj1.getmovie()
	data=obj1.getFavData()
	slist=obj1.slist

	if str(sid) in slist:
		slist.remove(str(sid))

	t.fav=','.join(slist)
	t.save()
	return redirect(request.META['HTTP_REFERER'])

def recent(request):
	obj1=SendRec(request)
	rdata=obj1.getRecData()
	rdata=dict(reversed(list(rdata.items())))
	print("RDICT",rdata)
	return render(request,'ht1/recent.html',{'rdata':rdata.values()})

def removeRecents(request,sid):
	t=User.objects.get(id=request.user.id)
	obj1=SendRec(request)
	recsongs=obj1.getrecsongs()
	mov=obj1.getrecmovie()
	data=obj1.getRecData()
	newsongslist=obj1.newsongslist
	print("IN REMOVE HERE",newsongslist)
	if str(sid) in newsongslist:
		newsongslist.remove(str(sid))
	print("REMOVE AFETR",newsongslist)
	t.rec=','.join(newsongslist)
	t.save()
	return redirect(request.META['HTTP_REFERER'])

def clearAllRecents(request):
	r=User.objects.get(id=request.user.id)
	r.rec=''
	r.save()
	return redirect(request.META['HTTP_REFERER'])

def download(request,path):
	file_path=os.path.join(settings.MEDIA_ROOT,path)
	if os.path.exists(file_path):
		with open(file_path,'rb') as fh:
			response=HttpResponse(fh.read(),content_type="application/song")
			response['Content-Disposition']='inline;filename='+os.path.basename(file_path)
			return response
	raise Http404
def sub(r):
	u=User.objects.get(id=r.user.id)
	if r.method=="POST":
		u.is_sub=1
		messages.success(r,"{} subscribed Successfully".format(u.username))
		u.save()
		return render(r,'ht1/sub.html')
		
	return render(r,'ht1/sub.html',{'u1':u})

def sublist(r):
	ur=User.objects.filter(is_sub=1)
	return render(r,'ht1/sublist.html',{'u1':ur})

