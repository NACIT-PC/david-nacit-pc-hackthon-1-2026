import random
from datetime import date

# Global list to store certificates
certificates_list = []

def verify_cert(cert_no: str):
    if cert_no[:3] in ['NCC', 'GRN']:
        return {"message": "Certificate number is valid."}
    else:
        return {"message": f"Certificate number: {cert_no} is invalid."}
     
def createCerficateNo():
    """
    Docstring for createCerficateNo
    Create a Valid Certificate Number
    The certificate number should be in the format:
    [Board][Centre][Year][Certificate ID]
    Where:
    - Board: A three-letter code representing the certifying board (e.g., "NCC", "GRN").
    - Centre: A single-digit code representing the examination centre (e.g., "0", "1").
    - Lilongwe = 0
    - Blantyre = 1
    - As we grow we can add more centres and assign them codes
    """
    board = random.choice(['NCC', 'GRN'])
    centre = random.choice(['0', '1'])
    year = random.randint(2021, 2026)
    cert_id = random.randint(00000, 99999)

    return f"{board}{centre}{year}{cert_id}"

def create_cert(name: str, middle_name: str, surname: str):
    cert_no = createCerficateNo()
    
    #Todays date
    today = date.today()

    # Generate a unique ID for the certificate
    cert_id = len(certificates_list) + 1

    cert = dict(
            id=cert_id,
            cert_no= cert_no,
            board=cert_no[:3],
            type="Diploma in Computing",
            school="NACIT",
            name=name,
            middle_name=middle_name,
            surname=surname,
            course="Software Development",
            date_of_issue=today,
            logo_url="https://nacit.co.mw/wp-content/uploads/2023/11/NACIT-LOGO.png",
        )
    
    # Add certificate to the global list
    certificates_list.append(cert)
    
    return cert

def list_certs():
    """
    Returns a list of all certificates
    """
    return certificates_list

def get_cert_by_no(cert_no: str):
    """
    Find and return a certificate by certificate number
    """
    for cert in certificates_list:
        if cert.get('cert_no') == cert_no:
            return cert
    return None

def get_certs_by_board(board: str):
    """
    Returns a list of certificates for a specific board
    """
    return [cert for cert in certificates_list if cert.get('board') == board]

def get_certs_by_name(name: str):
    """
    Returns a list of certificates for a specific name
    """
    return [cert for cert in certificates_list if cert.get('name').lower() == name.lower()]
