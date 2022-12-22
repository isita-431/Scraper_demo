import streamlit as st 
import pandas as pd 
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import sys
import os
import streamlit.components.v1 as stc
import matplotlib.pyplot as plt
import sqlite3
import csv
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
# from selenium_move_cursor.MouseActions import move_to_element_chrome
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
import traceback
import time
import sys
import os
import pandas as pd
# conn = sqlite3.connect('data.db',check_same_thread=False)
# cur = conn.cursor()
st.set_page_config(page_title='Scraper',layout='wide')

st.title('Scraper')

st.text('Please select one website')

option = st.selectbox(
    'Which website do you want to scrape data from ?',
    ('Lybrate', 'Credihealth'))

time.sleep(30)

st.write('You selected:', option)

def Driver():
    chrome_options = webdriver.ChromeOptions()
    output_path = os.path.join(os.getcwd(),'output')
    download_excel_prefs = {"download.default_directory" : output_path}
    chrome_options.add_experimental_option("prefs",download_excel_prefs)   
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--enable-popup-blocking")
    chrome_options.add_argument('--disable-notifications')
    chrome_path = ChromeDriverManager().install()
    driver=webdriver.Chrome(chrome_path,options=chrome_options)
    time.sleep(3)
    return driver

if option == 'Credihealth':
    # time.sleep(30)
    option3 = st.selectbox('Please select the specialization',('Cardiologist','Dermatologist','Cosmetology'))
    time.sleep(30)
    st.write('You selected:', option3)
    option2 = st.multiselect('Please select a Location you want to scrape data from',
    ['Hyderabad','Bangalore','Mumbai'])
    time.sleep(30)
    st.write('You selected:', option2)
    
    def credihealth(website,loc, key):
        doctor_name_l=[]
        personal_statement_l =[]
        specialization_l =[]
        Other_treatment_areas_l=[]
        qualifications_l= []
        experience_l=[]
        cost_l =[]
        Education_l=[]
        Past_Experience_l =[]
        Languages_spoken_l =[]
        Awards_and_Recognitions_l =[]
        Professional_Memberships_=[]
        rating_l =[]
        clinics_l = []
        speciality_l=[]
        doctor_links=[]
        
        for lo in loc:
            driver = Driver()
            driver.get('https://www.credihealth.com')
            #     driver.get('https://www.credihealth.com')
                # book_appointment = driver.find_element(By.XPATH,"//span[@ga-event='Book_Appointment']")
            time.sleep(4)
                # book_appointment.click()
            location = driver.find_element(By.XPATH,"//input[@placeholder='Choose City']")
            location.clear()
            location.send_keys(lo)
            time.sleep(2)
            location.send_keys(Keys.ENTER)
            time.sleep(4)
            keyword = driver.find_element(By.XPATH,"//input[@placeholder='Search Doctor, Hospital, Speciality or Treatment']")
            keyword.clear()
            keyword.send_keys(key)
            time.sleep(2)
            keyword.send_keys(Keys.ENTER)
            time.sleep(4)
            try:
                f=1
                blocks = driver.find_elements(By.XPATH,"//div[@class='display-inblock padding-l20 vertical-top mid_content']")
                for m in blocks:
                    doctor_links.append(m.find_element_by_tag_name('a').get_attribute('href'))
                        
                    doctor_name_l.append(m.find_element_by_tag_name('a').text)
                    specialization_l.append(key)
                next_l =[]
                while f:
                    try:
                        next_button = driver.find_element(By.XPATH,"//li[@class='next']")
                        time.sleep(2)
                        next_l.append(next_button.find_element_by_tag_name('a').get_attribute('href'))
                        time.sleep(2)
            #             print(next_l)
                        driver.get(next_button.find_element_by_tag_name('a').get_attribute('href'))
                    except:
                        f=0
                for i in next_l:
                    driver.get(i)
                    blocks = driver.find_elements(By.XPATH,"//div[@class='display-inblock padding-l20 vertical-top mid_content']")
                    for m in blocks:
            #         print(i.find_element_by_tag_name('a').get_attribute('href'))
            #         links.append(i.find_element_by_tag_name('a').get_attribute('href'))
                        doctor_links.append(m.find_element_by_tag_name('a').get_attribute('href'))
                            # doctor_links.extend(links_l)
                        doctor_name_l.append(m.find_element_by_tag_name('a').text)
                        specialization_l.append(key)
            except:
                print(traceback.format_exc())
            finally:
                driver.quit()
                    
            print(doctor_links)
            print(len(doctor_links)) 

            try:
                driver = Driver()
                for k in doctor_links:
                    driver.get(k)
                    p = driver.find_element(By.XPATH,"//a[@id='exp-toggel']")
                    print(p.text)
                    time.sleep(1)
                    try:
                        qual = driver.find_element(By.XPATH,"//p[@class='margin-0 margin-b10']")
                        qualifications_l.append(qual.text)
                        time.sleep(1)
                    except:
                        qualifications_l.append(' ')
                    try:
                        exp = driver.find_element(By.XPATH,"//p[@class='margin-b10 fw-500']")
                        time.sleep(1)
                        experience_l.append(exp.find_element_by_tag_name('span').text)
                    except:
                        experience_l.append(' ')
                    try:
                        ota = driver.find_element(By.XPATH,"//span[@class='color-555 margin-l10']")
                        time.sleep(1)
                        Other_treatment_areas_l.append(ota.text)
                    except:
                        Other_treatment_areas_l.append(' ')
                    try:
                        more = driver.find_element(By.XPATH,"//a[@class='border-none color-blue-128 fw-500 fs-13 button-view display-inline no-decoration cursor-pointer']")
                        time.sleep(1)
                        more.click()
                        des = driver.find_element(By.XPATH,"//div[@class='fs-14 color-555 text-justify description ']")
                        time.sleep(1)
                        personal_statement_l.append(des.text)
                    except:
                        personal_statement_l.append(' ')
                    try:
                        select_options =  driver.find_element(By.XPATH,"//select[@name='hospital_id']")
                        time.sleep(2)
                        ele= select_options.find_elements_by_tag_name('option')
                        time.sleep(2)
                        feee=[]
                        for j in ele:
                            j.click()
                            time.sleep(2)
                            print('---------------------------')
                            try:
                                fee = driver.find_element(By.XPATH,"//p[@class='margin-b0 pull-left margin-r10']")
                                time.sleep(2)
                                print(fee.text)
                                feee.append(fee.text)
                            except Exception as e:
                                feee.append(' ')
                        cost_l.append(feee)
                    except:
                        cost_l.append(' ')
                    time.sleep(1)
                    try:
                        clinics =[]
                        select_options =  driver.find_element(By.XPATH,"//select[@name='hospital_id']")
                        ele= select_options.find_elements_by_tag_name('option')
                        for i in ele:
                            clinics.append(i.text)
                        clinics_l.append(clinics)
                    except:
                        clinics_l.append('  ')
                    time.sleep(1)
                    try:
                        table = driver.find_element(By.XPATH,"//p[@class='fw-500 margin-0 margin-b10 fs-14']")
                        edu = table.find_elements(By.XPATH,"//p[@class='margin-0 fs-14 padding-b10 color-555']")
                        li =[]
                        for v in edu:
                            li.append(v.text)
                        Education_l.append(li)
                    except:
                        Education_l.append('  ')
                    time.sleep(1)
                    try:
                        time.sleep(2)
                        p.send_keys(Keys.ENTER)
                        time.sleep(2)
                        ele = driver.find_element(By.XPATH,"//div[@class='panel-body infotab__education-wrapper']")
                        time.sleep(2)
                        print(ele.text)
                        Past_Experience_l.append(ele.text)
                    except Exception as e:
                        driver.get(k)
                        p = driver.find_element(By.XPATH,"//a[@id='exp-toggel']")
                        p.send_keys(Keys.ENTER)
                        time.sleep(1)
                        ele = driver.find_element(By.XPATH,"//div[@class='panel-body infotab__education-wrapper']")
                        time.sleep(1)
                        print(ele.text)
                        Past_Experience_l.append(ele.text)
                    time.sleep(1)
                    try:
                        table = driver.find_element(By.XPATH,"//a[@id='awards-toggel']")
                        time.sleep(2)
                        table.send_keys(Keys.ENTER)
                        time.sleep(2)
                        awards = driver.find_elements(By.XPATH,"//div[@class='panel-body infotab__education-wrapper']")
                        time.sleep(2)
                        Awards_and_Recognitions_l.append(awards[1].text)
                    except:
                        driver.get(k)
                        time.sleep(2)
                        
                        print('------------------------')
                        try:
                            if driver.find_element(By.XPATH,"//a[@id='awards-toggel']"):
                                table = driver.find_element(By.XPATH,"//a[@id='awards-toggel']")
                                table.send_keys(Keys.ENTER)
                                awards = driver.find_elements(By.XPATH,"//div[@class='panel-body infotab__education-wrapper']")
                                time.sleep(2)
                                Awards_and_Recognitions_l.append(awards[1].text)
                        except:
                            Awards_and_Recognitions_l.append('  ')

            except Exception as e:
                print(traceback.format_exc())
            finally:
                driver.quit()
        df = pd.DataFrame({'links':doctor_links,'doctor_name':doctor_name_l ,'personal_statement': personal_statement_l,'specialization':specialization_l,'Other_treatment_areas':Other_treatment_areas_l,'qualifications':qualifications_l,'experience':experience_l,'cost': cost_l,
        'Education':Education_l,'Past_Experience':Past_Experience_l,'Awards_and_Recognitions':Awards_and_Recognitions_l,'clinics':clinics_l })
        # df.to_csv('Output/{}_{}_{}.csv'.format(website,loc,key))
        @st.cache
        def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')
        csv = convert_df(df)

        st.download_button(label="Download data as CSV",data= csv,file_name='{}_{}_{}.csv'.format(website,loc,key), mime='text/csv')
    credihealth(option,option2,option3)
    
    time.sleep(500)
 

if option == 'Lybrate':
    option4 = st.multiselect('Please select a Location you want to scrape data from',
    ['Hyderabad','Delhi','Mumbai'])
    st.write('You selected:', option4)
    time.sleep(30)
    option5 = st.selectbox('Please select the specialization',('Dentist','Cardiology','Gastroenterology'))
    st.write('You selected:', option5)
    time.sleep(30)
    li = []
    doctor_name_l=[]
    personal_statement_l =[]
    specialization_l =[]
    Other_treatment_areas_l=[]
    qualifications_l= []
    experience_l=[]
    cost_l =[]
    Education_l=[]
    Past_Experience_l =[]
    Languages_spoken_l =[]
    Awards_and_Recognitions_l =[]
    Professional_Memberships_=[]
    rating_l =[]
    clinics__l = []
    speciality_l=[]
    def lybrate(website,loc, k):
        # driver = Driver()
        for lo in loc:
            driver = Driver()
            driver.get('https://www.lybrate.com/')
            book_appointment = driver.find_element(By.XPATH,"//span[@ga-event='Book_Appointment']")
            time.sleep(3)
            book_appointment.click()
            location = driver.find_element(By.XPATH,"//input[@id='ex1_value']")
            location.clear()
            location.send_keys(lo)
            keyword = driver.find_element(By.XPATH,"//input[@id='ex3_value']")
            keyword.clear()
            keyword.send_keys(k)
            search_button = driver.find_element(By.XPATH,"//ly-svg-icon[@ga-event='Search']")
            search_button.click()
            time.sleep(5)
            page_links =[]
            page_links.append(driver.find_element(By.XPATH,"//a[@ga-event='Previous']").get_attribute('href'))
            flag=1
            while flag:
                try:
                    page_button = driver.find_element(By.XPATH,"//a[@ga-event='Next']")
                    time.sleep(1)
                    page_links.append(page_button.get_attribute('href'))
                    driver.get(page_button.get_attribute('href'))
                    time.sleep(1)
                except:
                    flag =0    
            page_links = page_links[:-1]
            print(page_links)
            links = []
            try:
                for i in page_links:        
                    driver.get(i)
                    time.sleep(1)
                    
                    find_doctor = driver.find_elements(By.XPATH,"//h2[@ng-if='ctrl.profile.name']")
                    time.sleep(5)
                    print(find_doctor)
                    for j in find_doctor:
                        links.append(j.find_element_by_tag_name('a').get_attribute('href'))
                    time.sleep(3) 
            except:
                print(traceback.format_exc())
            li.extend(links)

            try:
                for link in links: 
                    #     link = i.find_element_by_tag_name('a').get_attribute('href')
                    driver.get(link)
                #             action.move_by_offset(10, 20).perform()
                    src = driver.page_source
    
                    # # Now using beautiful soup
                    soup = BeautifulSoup(src, 'lxml')
                    try:
                        # click_more = driver.find_element(By.XPATH,"//span[@ng-click='ctrl.showMorePersonal()']")
                        # time.sleep(1)
                        # click_more.click()
                        # personal_statement = driver.find_element(By.XPATH,"//div[@id='moreProfessionalSummary']")
                        # time.sleep(3)
                        # print('bhbhbh'+personal_statement.text)
                        # personal_statement_l.append(personal_statement.text)
                        personal_statement_l.append(soup.find_all("div",{'id':"moreProfessionalSummary"})[0].text)
                    except:
                        print(traceback.format_exc())
                        personal_statement_l.append('  ')
                    print(personal_statement_l)
                #             try:
                #                 no_thanks = driver.find_element(By.XPATH,"//div[@ga-event='Other_Doctors_Popup_No_Thanks']")
                #                 time.sleep(3)
                #                 if no_thanks:
                #                     no_thanks.click()
                #             except:
                #                 pass
                    time.sleep(3)
                    try:
                        # name_doctor = driver.find_elements_by_class_name('lybMar-right')
                        time.sleep(3)
                        print(soup.find("h1",{'class':"lybMar-right"}).text.strip())
                        doctor_name_l.append(soup.find("h1",{'class':"lybMar-right"}).text.strip())
                        # name_doctor[0].text)
                        # print(name_doctor[0].text)
                    except:
                        doctor_name_l.append(' ')
                    try:
                        rating_doctor = driver.find_elements_by_class_name('lybText--green')
                        time.sleep(3)
                        rating_l.append(rating_doctor[1].text)
                    except:
                        rating_l.append(' ')
                    try:
                        # qualifications = driver.find_elements(By.XPATH,"//span[@class='lybText--light lybText--bold lybText--body']")
                        # 	# driver.find_element(By.XPATH,"//span[@ng-click='ctrl.showMorePersonal()']")
                        # 	# driver.find_element(By.XPATH,"//div[@id='moreProfessionalSummary']")
                        # time.sleep(3)
                        print(soup.find("span",{'class':"lybText--light lybText--bold lybText--body"}).text)
                        qualifications_l.append(soup.find("span",{'class':"lybText--light lybText--bold lybText--body"}).text)
                    except:
                        qualifications_l.append(' ')
                    try:
                        # specialization = driver.find_elements(By.XPATH,"//h2[@class='lybText--light lybText--bold lybText--body lybMar-btm--half']")
                        # # driver.find_element(By.XPATH,"//span[@ng-click='ctrl.showMorePersonal()']")
                        # # driver.find_element(By.XPATH,"//div[@id='moreProfessionalSummary']")
                        # time.sleep(3)
                        specialization_l.append(option5)
                        # driver.find_element(By.XPATH,"//span[@ng-click='ctrl.showMorePersonal()']")
                        # driver.find_element(By.XPATH,"//div[@id='moreProfessionalSummary']")
                    except:
                        specialization_l.append(' ')
                    
                    ye=0
                    c=0
                    cost =[]
                    try:
                        ele = soup.find_all("div",{'class':"lybMar-btm--half"})[2].text.split('\n')
                        for y in ele:
                            if 'Years' in y:
                                ye=1
                                experience_l.append(y)
                            if '₹' in y:
                                cost.append(y)
                                c=1
                        cost_l.append(cost)
                        print(cost_l)
                        print(experience_l)
                    except:
                        pass
            
                        # years = driver.find_elements(By.XPATH,"//div[@class='lybMar-btm--half']")
                        # time.sleep(3)
                        # y_text = years[0].text
                        # y_text = y_text.split('·')
                        # experience_l.append(y_text[0])
                        # cost =[]
                        # for cm in range(1, len(y_text)):
                        # 	cost.append(y_text[cm])
                        # cost_l.append(cost)
                        # time.sleep(2)
                    if ye==0:
                        experience_l.append('  ')
                    if c==0:
                        cost_l.append('  ')
                        # experience_l.append('  ')
                        # cost_l.append('  ')

                    try:
                        card2 = driver.find_elements(By.XPATH,"//div[@class='lybGutter lybMar-btm']")
                        # driver.find_element(By.XPATH,"//span[@ng-click='ctrl.showMorePersonal()']")
                        # driver.find_element(By.XPATH,"//div[@id='moreProfessionalSummary']")
                        time.sleep(5)
                        elements = card2[1].find_elements_by_class_name('lybMar-btm')
                        time.sleep(3)
                    except: 
                        elements =[]
                    f1,f2,f3,f4,f5,f6,f7 = 0,0,0,0,0,0,0
                    for s in elements:
                        titles = s.find_element_by_class_name('title')
                        time.sleep(1)
                        title = titles.text
                        if title == 'Speciality':
                            f1=1
                            spe =[]
                            eles= s.find_elements_by_class_name('items')
                            time.sleep(1)
                            for j in eles:
                                spe.append(j.text)
                            speciality_l.append(spe)
                        elif title == 'Other treatment areas':
                            f2=1
                            ota =[]
                            eles= s.find_elements_by_class_name('items')
                            time.sleep(1)
                            for j in eles:
                                ota.append(j.text)
                            Other_treatment_areas_l.append(ota)
                        if title == 'Education':
                            f3=1
                            edu = []
                            eles= s.find_elements_by_class_name('items')
                            time.sleep(1)
                            for j in eles:
                                edu.append(j.text)
                            Education_l.append(edu)
                        if title == 'Past Experience':
                            f4=1
                            exp = []
                            eles= s.find_elements_by_class_name('items')
                            time.sleep(1)
                            for j in eles:
                                exp.append(j.text)
                            Past_Experience_l.append(exp)
                        if title == 'Languages spoken':
                            f5=1
                            lang = []
                            eles= s.find_elements_by_class_name('items')
                            time.sleep(1)
                            for j in eles:
                                lang.append(j.text)
                            Languages_spoken_l.append(lang)
                        if title == 'Awards and Recognitions':
                            f6=1
                            awa = []
                            eles= s.find_elements_by_class_name('items')
                            time.sleep(1)
                            for j in eles:
                                awa.append(j.text)
                            Awards_and_Recognitions_l.append(awa)
                        if title == 'Professional Memberships':
                            f7=1
                            prof = []
                            eles= s.find_elements_by_class_name('items')
                            time.sleep(1)
                            for j in eles:
                                prof.append(j.text)
                            Professional_Memberships_.append(prof)
                    if f1 ==0:
                        speciality_l.append(' ')
                    if f2 ==0:
                        Other_treatment_areas_l.append(' ')
                    if f3 ==0:
                        Education_l.append(' ')
                    if f4 ==0:
                        Past_Experience_l.append(' ')
                    if f5 ==0:
                        Languages_spoken_l.append(' ')
                    if f6 ==0:
                        Awards_and_Recognitions_l.append(' ')
                    if f7 ==0:
                        Professional_Memberships_.append(' ')
                    clinics = driver.find_elements(By.XPATH,"//div[@class='lybMar-btm grid__col-20 grid--direction-column ly-doctor ng-isolate-scope']")
                            # driver.find_element(By.XPATH,"//span[@ng-click='ctrl.showMorePersonal()']")
                            # driver.find_element(By.XPATH,"//div[@id='moreProfessionalSummary']")
                    clinics_l=[]
                    time.sleep(2)
                    for c in clinics:
                        clinics_l.append(c.text)
                    clinics__l.append(clinics_l)

            except Exception as e:
                print(traceback.format_exc())
                pass
            finally:
                print('finished')
                # n = min(len(links),len(doctor_name_l),len(personal_statement_l),len(specialization_l),len(Other_treatment_areas_l),len(qualifications_l),len(experience_l),len(cost_l) ,len(Education_l),len(Past_Experience_l) ,len(Languages_spoken_l) ,len(Awards_and_Recognitions_l),len(Professional_Memberships_),len(rating_l) ,len(clinics__l) ,len(speciality_l))
                print(len(links),len(doctor_name_l),len(personal_statement_l),len(specialization_l),len(Other_treatment_areas_l),len(qualifications_l),len(experience_l),len(cost_l) ,len(Education_l),len(Past_Experience_l) ,len(Languages_spoken_l) ,len(Awards_and_Recognitions_l),len(Professional_Memberships_),len(rating_l) ,len(clinics__l) ,len(speciality_l))
                driver.quit()
                # print(n)
                # # print(len(n))
                # links = links[:n]
                # doctor_name_l = doctor_name_l[:n]
                # personal_statement_l = personal_statement_l[:n]
                # specialization_l = specialization_l[:n]
                # Other_treatment_areas_l = Other_treatment_areas_l[:n]
                # qualifications_l = qualifications_l[:n]
                # experience_l = experience_l[:n]
                # cost_l = cost_l[:n]
                # Education_l =Education_l[:n]
                # Past_Experience_l = Past_Experience_l[:n]
                # Languages_spoken_l = Languages_spoken_l[:n]
                # Awards_and_Recognitions_l = Awards_and_Recognitions_l[:n]
                # Professional_Memberships_ = Professional_Memberships_[:n]
                # rating_l = rating_l[:n]
                # clinics__l = clinics__l[:n]
                # speciality_l = speciality_l[:n]
        
        # print(len(doctor_name_l),len(personal_statement_l),len(specialization_l),
        # len(Other_treatment_areas_l),len(qualifications_l),len(experience_l),
        # len(cost_l) ,len(Education_l),len(Past_Experience_l) ,len(Languages_spoken_l) ,len(Awards_and_Recognitions_l),
        # len(Professional_Memberships_),len(rating_l) ,
        # len(clinics__l) ,len(speciality_l))
        # n = min(len(links),len(doctor_name_l),len(personal_statement_l),len(specialization_l),
        # len(Other_treatment_areas_l),len(qualifications_l),len(experience_l),
        # len(cost_l) ,len(Education_l),len(Past_Experience_l) ,len(Languages_spoken_l) ,len(Awards_and_Recognitions_l),
        # len(Professional_Memberships_),len(rating_l) ,
        # len(clinics__l) ,len(speciality_l))
        # print(len(n))

    lybrate(option,option4,option5)
    df = pd.DataFrame({'links':li,'doctor_name': doctor_name_l, 'rating':rating_l,'personal_statement': personal_statement_l,'specialization':specialization_l,'Other_treatment_areas':Other_treatment_areas_l,'qualifications':qualifications_l,'experience':experience_l,'cost': cost_l,'Education':Education_l,'Past_Experience':Past_Experience_l,
        'Awards_and_Recognitions':Awards_and_Recognitions_l, 'clinics':clinics__l})

    @st.cache
    def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

    csv = convert_df(df)

    st.download_button(label="Download data as CSV",data= csv,file_name='{}_{}_{}.csv'.format(option,option4,option5), mime='text/csv')






        
        
        


