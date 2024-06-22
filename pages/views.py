#start libraries of django
from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
#end libraries of django
from .models import User,Company,Contactus,ContactusCom,ContactusUser,SearchEmployees,login,DataOfCV,Result
#start libraries of AI
from pdfminer.high_level import extract_text
import pytesseract
import pandas as pd
import PIL.Image
import io
import os
import cv2
import glob
import fitz
#end start libraries of AI


# Create backend code 


#start code AI 
def CheckTypeFile(path):
    if path[len(path)-3:].lower() in ['jpeg','png','jpg']:
        return AIReadIMAGES(path)
    elif path[len(path)-3:].lower() == 'pdf' :
        return AIReadPDF(path)
    else:
        return  ""


def AIReadIMAGES(path):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\\tesseract.exe'
    img = cv2.imread(path)
    img_text = pytesseract.image_to_string(img).lower().replace('\n', ' ')
    return img_text

def AIReadPDF(path):
    pdf = fitz.open(path)
    imageIndex = 1
    all_text_pdf = extract_text(path).lower().replace('\n', ' ')
    for i in range(len(pdf)):
        page = pdf[i]
        images = page.get_images()
        for imag in images:
            base_img = pdf.extract_image(imag[0])
            image_data = base_img['image']
            img = PIL.Image.open(io.BytesIO(image_data))
            extension = base_img['ext']
            # save image
            img.save(open(f'image{imageIndex}.{extension}', 'wb'))
            # path the image
            path_of_image = f'image{imageIndex}.{extension}'
            # read text from image
            img_text_png = AIReadIMAGES(path_of_image)
            # check if image contain on text
            if img_text_png != '':
                # add text image in all text
                all_text_pdf += ' ' + img_text_png
            # delete image
            os.remove(path_of_image)
            # number of image
            imageIndex += 1
    return all_text_pdf

def titles(jobtitle,datacv,all_data_filter):
    dataset = pd.read_excel('DataSet.xlsx')
    setdataset = set(map(str,dataset['DataSet']))
    count = 0
    for title in jobtitle:
        if title.lower() in setdataset:
            if title.lower() in datacv.text:
                count += int((len(all_data_filter)+len(jobtitle))/2)
                break
            else:
                continue
        else:
            continue
    return count


def AnalyseDataPdf(lang,title,deg):
    languages = lang.split(',')
    jobtitle = title.split(',')
    degree = deg.split(',')
    all_data_filter = languages + degree
    data_of_cv = DataOfCV.objects.all()
    list_result = []
    set_filter = {}
    count = 0
    for datacv in data_of_cv:
        count += titles(jobtitle,datacv,all_data_filter)
        if count != 0 :
            for datafilter in all_data_filter:
                if datafilter.strip().lower() in datacv.text:
                    if set_filter.get(datafilter) == None:
                        set_filter.setdefault(datafilter,1)
                        count += 1
                        continue  
            percentage = (count /len(all_data_filter)) * 100 
            if percentage >= 60:
                list_result.append(datacv.e_mail)
                if percentage > 100 :
                    percentage = 100
                User.objects.filter(e_mail = datacv.e_mail).update(rate=round(percentage))
        else:
            count = 0
            set_filter = {}
            continue
        count = 0
        set_filter = {}
    return list_result


def ResultOfAI(email,url):
    files = glob.glob("media/*")
    path_file = str(url[1:])
    data_of_cv = CheckTypeFile(path_file)
    DataOfCV.objects.create(text=data_of_cv,e_mail=email)
#end code AI 



#===============HomePage=====================

def Homepage(request):
    if  login.objects.count() > 0:
        login.objects.all().delete() 
    return render(request,'pages/Homepage.html')


def contactus(request):  
    if  login.objects.count() < 1:
        if request.method == 'POST': 
            name = request.POST['name']
            email = request.POST['email']
            message = request.POST['message']
            Contactus.objects.create(Name=name,e_mail=email,Message=message)
            return redirect('Homepage')
        return render(request,'pages/contactus.html')
    else:
        return render(request,'pages/Homepage.html')
    

def loginpage(request):
    if request.method == 'POST':  
        if  login.objects.count() < 1:
            email = request.POST['Email']
            pass_word = request.POST['password']
            if bool(User.objects.filter(e_mail = email,Password=pass_word)) :
                login.objects.create(e_mail=email)
                return redirect('HomeUser')
            elif bool(Company.objects.filter(e_mail = email,Password=pass_word)) :
                login.objects.create(e_mail=email)
                return redirect('HomeCom')
            return redirect('loginpage')
        return redirect('Homepage')
    return render(request,'pages/loginpage.html')


def SignupUser(request):
    if request.method == 'POST': 
        if  login.objects.count() < 1:
            name = request.POST['signup_UserName']
            email = request.POST['signup_Email']
            uploaded_file = request.FILES['Signup_cv']
            password = request.POST['signup_Password']
            re_password = request.POST['Repeat_Password']
            if not bool(User.objects.filter(e_mail = email)):
                if password == re_password:
                    fs = FileSystemStorage()
                    fs.save(uploaded_file.name, uploaded_file)
                    url = fs.url(uploaded_file.name)
                    ResultOfAI(email,url)
                    User.objects.create(username=name,e_mail=email,Password=password,filepdf=uploaded_file)
                    return redirect('loginpage')
                return redirect('SignupUser')
            return redirect('SignupUser')
        else:
            return redirect('Homepage')
    else:
        return render(request,'pages/SignupUser.html')

    

def SignupCompany(request):
    if request.method == 'POST':
        if  login.objects.count() < 1: 
            name = request.POST['signup_CompanyName']
            email = request.POST['signup_Email']
            password = request.POST['signup_Password']
            re_password = request.POST['Repeat_Password']
            if not bool(Company.objects.filter(companyname = name)) and not bool(Company.objects.filter(e_mail = email)):
                if password == re_password:
                    Company.objects.create(companyname=name,e_mail=email,Password=password)
                    return redirect('loginpage')
                return redirect('SignupCompany')
            return redirect('SignupCompany')
        else:
            return redirect('Homepage')
    else:
        return render(request,'pages/SignupCompany.html')
    



#===============Company=====================

def HomeCom(request):
    if  login.objects.count() > 0 :
        return render(request,'pages/HomeCom.html')
    else:
        return redirect('loginpage')


def ProfileCompany(request):
    if request.method == "POST":
        return redirect('EditeDataCom')
    if  login.objects.count() > 0:
        data = login.objects.first()
        for i in Company.objects.all():
            if i.e_mail == data.e_mail:
                data_company = i
                break
        return render(request, 'pages/ProfileCompany.html',{'data':data_company})
    else:
        return redirect('loginpage')
    

def resultsearchemployee(request):
    if  login.objects.count() > 0:
        return render(request, 'pages/resultsearchemployee.html')
    else:
        return redirect('loginpage')
    

def employeer(request):
    if  login.objects.count() > 0 :
        data = login.objects.first()
        if request.method == 'POST': 
            title =  request.POST['jobTitle']
            expe = request.POST['experience']
            lang = request.POST['languages']
            deg = request.POST['degree']
            email = data.e_mail
            result = AnalyseDataPdf(lang,title,deg)
            lest = []
            if result != []:
                for i in User.objects.all():
                    if i.e_mail in result:
                        lest.append(i)
                SearchEmployees.objects.create(jobtitle=title,e_mail=email,languages=lang,degree=deg,experience=expe)
                return render(request,'pages/resultsearchemployee.html',{'data':lest})
            else:
                messages.error(request, 'No employees found matching the search criteria.')
                return render(request, 'pages/employeer.html')
        else:
            return render(request,'pages/employeer.html')
    else:
        return redirect('loginpage')


def contactusCom(request): 
    if request.method == 'POST': 
        if  login.objects.count() > 0: 
            name = request.POST['name']
            email = request.POST['email']
            message = request.POST['message']
            if bool(Company.objects.filter(e_mail = email)) :
                ContactusCom.objects.create(Name=name,e_mail=email,Message=message)
                return redirect('HomeCom')
            return redirect('contactusCom')
        else:
            return redirect('Homepage')
    return render(request,'pages/contactusCom.html')


def EditeDataCom(request):
    if 'Edite_companyname' in request.POST:
        if request.method == 'POST':
            name = request.POST['Edite_companyname']
            email = request.POST['up_email']
            Company.objects.filter(e_mail = email).update(companyname=name)
            return redirect('ProfileCompany')
        else:
            return redirect('EditeDataCom')
    else:
        data = login.objects.first()
        for i in Company.objects.all():
            if i.e_mail == data.e_mail:
                data_company = i
                break
        return render(request,'pages/EditeDataCom.html',{'data':data_company})



#===============User=====================

def HomeUser(request):
    if  login.objects.count() > 0:
        return render(request,'pages/HomeUser.html')
    else:
        return redirect('loginpage')



def ProfileUser(request):
    if request.method == "POST":
        return redirect('EditeDataUser')
    else:
        if  login.objects.count() > 0:
            data = login.objects.first()
            for i in User.objects.all():
                if i.e_mail == data.e_mail:
                    data_user = i
                    break
            return render(request, 'pages/ProfileUser.html',{'data':data_user})
        else:
            return redirect('loginpage')


def contactusUser(request):  
    if request.method == 'POST': 
        if  login.objects.count() > 0 : 
            name = request.POST['name']
            email = request.POST['email']
            message = request.POST['message']
            if bool(User.objects.filter(e_mail = email)) :
                ContactusUser.objects.create(Name=name,e_mail=email,Message=message)
                return redirect('HomeUser')
            return redirect('contactusUser')
        else:
            return redirect('Homepage')
    return render(request, 'pages/contactusUser.html')



def EditeDataUser(request):
    if 'Edite_UserName' in request.POST:
        if request.method == 'POST':
            name = request.POST['Edite_UserName']
            email = request.POST['up_email']
            if bool(request.FILES):
                DataOfCV.objects.filter(e_mail=email).delete()
                uploaded_file = request.FILES['Edite_cv']
                fs = FileSystemStorage()
                fs.save(uploaded_file.name, uploaded_file)
                url = fs.url(uploaded_file.name)
                ResultOfAI(email,url)
                User.objects.filter(e_mail = email).update(username=name,filepdf=uploaded_file)
                return redirect('ProfileUser') 
            else:
                User.objects.filter(e_mail = email).update(username=name)
                return redirect('ProfileUser')
        else:
            return redirect('EditeDataUser')
    else:
        data = login.objects.first()
        for i in User.objects.all():
            if i.e_mail == data.e_mail:
                data_user = i
                break
        return render(request,'pages/EditeDataUser.html',{'data':data_user})