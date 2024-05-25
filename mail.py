import urllib.request
import urllib.parse
import json


LICENSE_KEY = "Xx5BkbONBbOxPtIfCzTp7j**nSAcwXpxhQ0PC2lXxuDAZ-**"
URL = "https://globalemail.melissadata.net/v4/WEB/GlobalEmail/doGlobalEmail"
OPT = "VerifyMailBox:Express,DomainCorrection:off,TimeToWait:30,WhoIs:off"

def verify_email(key: str, mail: str,*, mailbox: str = "Express", dc: str = "off", wait: int = 30, whoIs: str = "off", format: str = "json"):

    params = urllib.parse.urlencode([('t', key), ('id', LICENSE_KEY), 
                                     ('opt', f"VerifyMailBox:{mailbox}, DomainCorrection:{dc}, TimeToWait:{wait}, whoIs:{whoIs}"),
                                    ('email', mail), ("format", format)])
    
    url = URL + '?' + params
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)

    data = response.read()
    response.close()
    text = data.decode(encoding = 'utf-8')
    result = json.loads(text)

    validity = "ES01" in result["Records"][0]["Results"]
    return validity


#print(verify_email("testingvalid", "brandonhoang7541@gmail.com"))
#print(verify_email("testinginvalid", "dasjkhsgkalhj@jljghsl.com"))

# Formatting Reference of search return

'''
{
  "Version": "8.4.1.4305",
  "TransmissionReference": "somethingfine",
  "TransmissionResults": "",
  "TotalRecords": "1",
  "Records": [
    {
      "RecordID": "1",
      "DeliverabilityConfidenceScore": "97",
      "Results": "ES01,ES21",
      "EmailAddress": "brandokh@uci.edu",
      "MailboxName": "brandokh",
      "DomainName": "uci",
      "DomainAuthenticationStatus": "SPF",
      "TopLevelDomain": "edu",
      "TopLevelDomainName": "Education",
      "DateChecked": "5/25/2024 4:41:11 PM",
      "EmailAgeEstimated": "0",
      "DomainAgeEstimated": "14110",
      "DomainExpirationDate": "2024-07-31T00:00:00",
      "DomainCreatedDate": "1985-09-30T00:00:00",
      "DomainUpdatedDate": "2023-06-16T00:00:00",
      "DomainEmail": "",
      "DomainOrganization": "",
      "DomainAddress1": "",
      "DomainLocality": "Irvine",
      "DomainAdministrativeArea": "CA",
      "DomainPostalCode": "92697-1175",
      "DomainCountry": "UNITED STATES",
      "DomainAvailability": "UNAVAILABLE",
      "DomainCountryCode": "US",
      "DomainPrivateProxy": "",
      "PrivacyFlag": "N",
      "MXServer": "",
      "DomainTypeIndicator": "Business/Organization",
      "BreachCount": ""
    }
  ]
}
'''
