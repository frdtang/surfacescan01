from flask import Flask, request
from app.measure import Disk_Surface
app = Flask(__name__)
 
@app.route('/distance', methods = ["GET"])
def distance():
    '''
    '''
    disk_surface = Disk_Surface()
    disk_surface.measure()    
    return disk_surface.distance,\
        200, {'ContentType': 'application/json'}

