from pyresparser import ResumeParser
data = ResumeParser('C:/Users/karim/OneDrive/Desktop/capstone/resume_scraper/karim_soubra_resume.pdf').get_extracted_data()

print(data)