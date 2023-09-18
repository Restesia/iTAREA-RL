from flask import Flask, Response
import datetime

app = Flask(__name__)

def saveAll():
    # Name file
    now = datetime.datetime.now()
    day = str(now.day).zfill(2)
    month = str(now.month).zfill(2)
    year = str(now.year)[-2:]
    hours = str(now.hour).zfill(2)
    minutes = str(now.minute).zfill(2)
    filename = f'{day}-{month}-{year}_{hours}.{minutes}.txt'
    
    # Content for the file
    result_data = "Your file content here."
    
    # Create a response with the file content
    response = Response(result_data, content_type='text/plain')
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    
    return response

if __name__ == '__main__':
    save_file()