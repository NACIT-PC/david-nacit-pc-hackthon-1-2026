from fastapi import FastAPI
from datetime import date
import random
import logic
from security import Security
from pydantic import BaseModel

app = FastAPI()


@app.get("/cert/verify/{cert_no}")
def read_root(cert_no: str):
   #security_obj = Security()
   #attempts = security_obj.track_attempts(cert_no)
        return logic.verify_cert(cert_no)

class Certificate(BaseModel):
    name: str
    middle_name: str
    surname: str
  
    

@app.post("/cert/generate")
async def read_root(certificate: Certificate):
    cert = logic.create_cert(certificate.name, certificate.middle_name, certificate.surname)
    return {"message": f"Generated certificate number: {cert}"}

@app.get("/cert/{cert_no}")
def read_root(cert_no: str):
    
    cert = logic.get_cert_by_no(cert_no)
    if cert:
        return {"message": cert}
    else:
        return {"message": f"Certificate number: {cert_no} is invalid."}