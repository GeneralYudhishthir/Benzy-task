from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('canteen_report')  
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')  

from django.shortcuts import render
import requests
from datetime import datetime

def get_canteen_report(request):
    url = 'http://canteen.benzyinfotech.com/api/v3/customer/report'
    headers = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiZWRhNWExODU0OTFhYWE0MmY5YzMyZjRhMTU5MDM1ODk4ZjZiMzMxNWUzZjJjNGRiZDA1N2IyNGE3NTAzMDc3NDBlMjFlYjZmNGE4Mjk0MGUiLCJpYXQiOjE3MDQ4MDA4OTAuODc5OTI1OTY2MjYyODE3MzgyODEyNSwibmJmIjoxNzA0ODAwODkwLjg3OTkyOTA2NTcwNDM0NTcwMzEyNSwiZXhwIjoxNzM2NDIzMjkwLjgzNDkxMjA2MTY5MTI4NDE3OTY4NzUsInN1YiI6IjI2NSIsInNjb3BlcyI6W119.CwDEjlHoRtOXdFcaO6KGGxV202AOA7MMtJVPtKzgLqzTFzUUnDLGBd7PNAtHO2--3YOathM9HOG8hYjY8wjktXZIoCGUR9GWIaEVUxLwFq927CrSf05NuqTBTrJcDeBOjXDvKcSBiJ2A994FC2IunPcdkaZ4jpoaWBIaWueYUbHviYSQuLec3tFcAMg4njrImAlaN9k-QKkHetpdrdbUEX1Wzq4X-1QwuOx7W3W2nbbxaoNgFX1gaabxi00ZO7h5MokGvtqy_gCkS9TYoM74VfxmTyAAczjttLcPqDNiAL_ZJdutDMezw32CZj8G8l8PUL46F_BuaxatZDBUZxeClZh4_0Wvo9GX4zqF2XvHdzZHnwdB414vNCl8itaGW9w7QWbdchPOglhnek32ZmkH0MIqeOBhnAyHo5_WbP0uLd_3qmz3w04nvTbTGV25-QebaxPAsVD0-7Za1sVpqB_FD6yEeliaEzdxl_8gA5IH59uowpfPYgUIjom8NVEASuYsAwb0q3f0jhNRfwg2zmXNenoDunh_dN9l2NRjI2gdZueSMwu6IJLQK46jpn01uG2iQ1xx-pFJAGe_bzSceLsho3dbtabym3tMqi0Ac02xUP9Mn50LdkFJGNVU9jiuHQfyjQirDtGUfya3aIvpJlCGx9Cx99s_4P89uDnOiXy3A1Q',
        'Content-Type': 'application/json',
        'Cookie': 'XSRF-TOKEN=eyJpdiI6InVqMzlHS1Z2YWRwSkRrd3Fwc3BMQUE9PSIsInZhbHVlIjoiNE5FU0IrMWhPMERsb213QVFoQ3BYc3VMUTNBMCswR2ErWDFkVUVmV2NXV2RQU2VwR1Fkb3lLNWx3ZVpGbnExcXZSd29zVTVLZ1BRQWF0ME1sNjkrc3dpaGVrSEl2QnFocTBEM0FaUThuc2ZLbnBOaFI3WXFNeTNDZFFTMnV3SU8iLCJtYWMiOiI1YmQ5OTM5Yjg4NGE2ZWY2YjgwNGRkYzRkOGNkMDQ5Mjc1MmRmMjcxMWJjNzkyOTBlY2MxZjliNDUyMGJlMTRhIiwidGFnIjoiIn0%3D; canteen_session=eyJpdiI6Imx5TXhDemlJMVE5UE05MFEvWjV6elE9PSIsInZhbHVlIjoiVmYva2Y2QVZGZkVSN3ZQL0lHaHR1RkVRaGlzeWs3TVVnbk01WFpsejB1SUxubXB1TE9GOFgvNEZVSjltQlF5UjY4UVloRDczWHNHOStHbE9LeUgxeWVnWXpQbDhrUUVTczdmMXNWOG5YR2VGZ0pLZWNuYXJYemdoaUpVRDZ5T0ciLCJtYWMiOiJhM2YyMmEwOTZmYjA3NjMwYWQ2NTVkNDM0MTAyZjJhZWVkZDczZjJjMTVkNjFmOWUyNjU5MDdkMDY4OGNlNDM1IiwidGFnIjoiIn0%3D'
    }

    month = request.GET.get('month')
    if not month:
        month = datetime.now().month  
    
    data = {
        "month": int(month)
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  
        report_data = response.json()
        
        user = report_data.get('user', {})
        reports = report_data.get('reports', [])
        
        return render(request, 'canteen_report.html', {'user': user, 'reports': reports, 'selected_month': int(month)})
    
    except requests.exceptions.HTTPError as err:
        return render(request, 'canteen_report.html', {'error': f"HTTP Error: {err}", 'selected_month': int(month)})
    
    except requests.exceptions.RequestException as e:
        return render(request, 'canteen_report.html', {'error': f"Request Error: {e}", 'selected_month': int(month)})
    
    return render(request, 'canteen_report.html', {'error': 'An unexpected error occurred.', 'selected_month': int(month)})


    

 