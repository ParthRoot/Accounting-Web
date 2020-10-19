from django.shortcuts import render
import pyrebase
from django.contrib import auth
from django.http import HttpResponse
from django.views.generic import View
from django.template.loader import get_template

from .utils import render_to_pdf  # created in step 4

# class GeneratePDF(View):


'''
def generate_view(request, *agrs, **kwargs):
    template = get_template("invoice.html")
    context = {
        "invoice_id": 123,
        "customer_name": "Parth Patel",
        "amount": 100,
        "today": "Sunday"
    }
    html = template.render(context)
    return HttpResponse(html)
'''

# Your web app's Firebase configuration

firebaseConfig = {
    "apiKey": "AIzaSyCvgUVTJSuaoRof4McNlmmdGQf5dwcmEng",
    "authDomain": "jaiminpateloffice-b7655.firebaseapp.com",
    "databaseURL": "https://jaiminpateloffice-b7655.firebaseio.com",
    "projectId": "jaiminpateloffice-b7655",
    "storageBucket": "jaiminpateloffice-b7655.appspot.com",
    "messagingSenderId": "890646554615",
    "appId": "1:890646554615:web:2204e2d15e44d8ac5af0f2"
};
# Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig)

# Get a reference to the auth service
authe = firebase.auth()

# Get a reference to the database service
db = firebase.database()


# Login Page

def voucherslogin(request):
    return render(request, "accounting/voucherslogin.html")


def ledgerlogin(request):
    return render(request, "accounting/ledgerlogin.html")


def tjledgerlogin(request):
    return render(request, "accounting/tjledgerlogin.html")


def tjlogin(request):
    return render(request, "accounting/tjlogin.html")


def creditlogin(request):
    return render(request, "accounting/creditlogin.html")


def tjcreditlogin(request):
    return render(request, "accounting/tjcreditlogin.html")


def debitlogin(request):
    return render(request, "accounting/debitlogin.html")


def tjdebitlogin(request):
    return render(request, "accounting/tjdebitlogin.html")


def reportlogin(request):
    return render(request, "accounting/reportlogin.html")


# index page
def index(request):
    return render(request, "accounting/index.html")


# about page
def about(request):
    return render(request, "accounting/about.html")


# message page
def message(request):
    return render(request, "accounting/message.html")


# corpotation page
def corporation(request):
    return render(request, "accounting/corporation.html")


# Login Authetication

def vouchersentry(request):
    email = request.POST.get('uname')
    passw = request.POST.get('pass')

    try:
        user = authe.sign_in_with_email_and_password(email, passw)
    except:
        return render(request, "accounting/vouchersloginerror.html")

    print(user['idToken'])
    session_id = user['idToken']
    request.session['uid'] = str(session_id)

    return render(request, "accounting/vouchersentry.html", {"e": email})


def ledger(request, null=""):
    email = request.POST.get('uname')
    passw = request.POST.get('pass')

    try:
        user = authe.sign_in_with_email_and_password(email, passw)
    except:
        return render(request, "accounting/ledgerloginerror.html")
    '''
       mix = mix date
       bill = script
       date = date
       amount = tjamount(negative)
       camount = tjamount(positive)
       ccamount = credit amount
       vamount = vouchers amount
       damount = debut amount
       rnb = runnung balance
       '''

    # mix
    mix = db.child("Mix").shallow().get().val()

    mix1 = []
    for i in mix:
        mix1.append(i)
    mix1.sort()

    # bill
    bill = []

    for i in mix1:
        bill1 = db.child('Mix').child(i).child('Script').get().val()

        a = bill1.upper()

        bill.append(a)
    # bill.sort(reverse=True)

    ccamount = []
    amount = []
    camount = []

    # tjamount(negative)
    for i in mix1:
        amount1 = db.child('Mix').child(i).child('Amount').get().val()
        if amount1 != None:
            if amount1 < 0:
                camount.append("")
                amount.append(abs(amount1))
            else:
                camount.append(amount1)
                amount.append("")

        else:
            amount.append("")
            camount.append("")
    # amount.sort(reverse=True)

    # tjamount(positive)
    for i in mix1:
        amount1 = db.child('Mix').child(i).child('CAmount').get().val()
        if amount1 != None:
            ccamount.append(amount1)
        else:
            ccamount.append("")
    # amount.sort(reverse=True)

    # Debit Amount
    damount = []
    for i in mix1:
        amount1 = db.child('Mix').child(i).child('DAmount').get().val()
        if amount1 != None:
            damount.append(amount1)
        else:
            damount.append("")
    # amount.sort(reverse=True)

    # vouchers amount
    vamount = []
    for i in mix1:
        amount1 = db.child('Mix').child(i).child('VAmount').get().val()
        if amount1 != None:
            vamount.append(amount1)
        else:
            vamount.append("")
    # amount.sort(reverse=True)

    # date
    date = []
    for i in mix1:
        date1 = db.child('Mix').child(i).child('Date').get().val()
        date.append(date1)
    # date.sort(reverse=True)

    # runing balance
    rnb = 0
    rnbl = []

    comb_list1 = zip(mix, bill, date, amount, camount, ccamount, vamount, damount)
    for m, b, d, a, ca, cca, v, d1 in comb_list1:
        if a != "":
            rnb = rnb - a
            rnbl.append(rnb)
        elif ca != "":
            rnb = rnb + ca
            rnbl.append(rnb)
        elif cca != "":
            rnb = rnb + cca
            rnbl.append(rnb)
        elif v != "":
            rnb = rnb - v
            rnbl.append(rnb)
        elif d1 != "":
            rnb = rnb - d1
            rnbl.append(rnb)

    # running balance total
    print(rnbl)
    rn = 0
    for i in rnbl:
        rn = rn + i
    print(rn)

    # Debit Amount Total
    combsumd = zip(amount, vamount, damount)
    dsum = 0
    for i, j, k in combsumd:
        if k != "":
            dsum = dsum + k
        elif j != "":
            dsum = dsum + j
        elif i != "":
            if i < 0:
                dsum = dsum - i
            else:
                dsum = dsum + i

    # Credit Amount Total

    combsumc = zip(ccamount, camount)
    csum = 0
    for i, j in combsumc:
        if j != "":
            csum = csum + j
        elif i != "":
            csum = csum + i

    comb_list = zip(mix, bill, date, amount, camount, ccamount, vamount, damount, rnbl)
    return render(request, "accounting/ledger.html", {"comb_list": comb_list, "dsum": dsum, "csum": csum, "rn": rn})


def tjledger(request):
    email = request.POST.get('uname')
    passw = request.POST.get('pass')

    try:
        user = authe.sign_in_with_email_and_password(email, passw)
    except:
        return render(request, "accounting/tjledgerloginerror.html")
    mix = db.child("Mixtj").shallow().get().val()

    date = []  # all dates
    scriptl = []  # script tjcredit or tjdebit
    tjcamountl = []  # amount tjcredit
    tjdamountl = []  # amount tjdebit
    ldate = []  # display date in ledger
    amount1 = []
    pamount = []  # trading journal positive amount
    namount = []  # trading journal negative amount
    rnbl = []  # running balance for trading journal ledger

    for i in mix:
        date.append(i)
    date.sort()

    for i in date:
        script = db.child("Mixtj").child(i).child("Script").shallow().get().val()
        tjcamount = db.child("Mixtj").child(i).child("tjcAmount").shallow().get().val()
        tjdamount = db.child("Mixtj").child(i).child("tjdAmount").shallow().get().val()
        amount = db.child("Mixtj").child(i).child("Amount").shallow().get().val()
        dat = db.child("Mixtj").child(i).child("Date").shallow().get().val()

        # script
        a = script.upper()
        scriptl.append(a)  # insert script(tj debit and tjcredit) in list

        # credit amount
        if tjcamount == None:
            tjcamountl.append("")
        else:
            tjcamountl.append(tjcamount)

        # debit amount
        if tjdamount == None:
            tjdamountl.append("")
        else:
            tjdamountl.append(tjdamount)

        # ldate
        ldate.append(dat)
        date.sort()

        # trading journal amount
        if amount == None:
            amount1.append("")
        else:
            amount1.append(amount)

    for i in amount1:
        if i == "":
            pamount.append(i)
            namount.append(i)
        elif i < 0:
            pamount.append("")
            namount.append(abs(i))
        else:
            pamount.append(i)
            namount.append("")

    comb_list1 = zip(ldate, scriptl, tjcamountl, tjdamountl, pamount, namount)
    rnb = 0
    for d, s, c, d, p, n in comb_list1:
        if c != "":
            rnb = rnb + c
            rnbl.append(rnb)
        elif d != "":
            rnb = rnb - d
            rnbl.append(rnb)
        elif p != "":
            rnb = rnb + p
            rnbl.append(rnb)
        elif n != "":
            rnb = rnb - n
            rnbl.append(rnb)
        else:
            pass
    rn = 0
    for i in rnbl:
        rn = rn + i

    # Debit Amount Total
    dsum = 0
    dcomb = zip(tjdamountl, namount)
    for i, j in dcomb:
        if j != "":
            if j < 0:
                dsum = dsum - j
            else:
                dsum = dsum + j
        elif i != "":
            dsum = dsum + i

    # Credit Amount Total
    csum = 0
    ccomb = zip(tjcamountl, pamount)
    for i, j in ccomb:
        if j != "":
            csum = csum + j
        elif i != "":
            csum = csum + i

    comb_list = zip(ldate, scriptl, tjcamountl, tjdamountl, pamount, namount, rnbl)
    return render(request, "accounting/tjledger.html", {"comb_list": comb_list, "dsum": dsum, "csum": csum, "rn": rn})


def report1(request):
    a = request.POST.get("ls")
    s = request.POST.get("sdate")
    e = request.POST.get("edate")

    global a2, s2, e2
    a2, s2, e2 = a, s, e

    # vouchers
    if a == "VOUCHERS":
        v = db.child("Vouchers").shallow().get().val()
        vl = []
        datel = []
        scriptl = []
        amountl = []
        vsum = 0
        for i in v:
            vl.append(i)
        vl.sort()
        for i in vl:

            vm = max(vl)
            vn = min(vl)

            if i >= s and i <= e and e > s:

                date = db.child("Vouchers").child(i).child("Date").shallow().get().val()
                datel.append(date)

                script = db.child("Vouchers").child(i).child("Script").shallow().get().val()
                a = script.upper()
                scriptl.append(a)

                amount = db.child("Vouchers").child(i).child("VAmount").shallow().get().val()
                amountl.append(amount)

                vsum = vsum + amount
                comb_list = zip(vl, datel, scriptl, amountl)

            elif s == e:
                if s in i:
                    date = db.child("Vouchers").child(i).child("Date").shallow().get().val()
                    datel.append(date)

                    script = db.child("Vouchers").child(i).child("Script").shallow().get().val()
                    a = script.upper()
                    scriptl.append(a)

                    amount = db.child("Vouchers").child(i).child("VAmount").shallow().get().val()
                    amountl.append(amount)

                    vsum = vsum + amount
                comb_list = zip(vl, datel, scriptl, amountl)  # vouchers



            elif e < vn:
                msg = "Select Valid date"
                return render(request, "accounting/report.html", {"msg": msg})

            elif e < s:
                msg = "End Date < Start Date"
                return render(request, "accounting/report.html", {"msg": msg})

            elif s > vm:
                msg = "Select Valid date"
                return render(request, "accounting/report.html", {"msg": msg})

        return render(request, "accounting/report1.html", {"comb_list": comb_list, "vsum": vsum})


    # debit
    elif a == "DEBIT":

        d = db.child("Debit").shallow().get().val()
        dl = []
        ddatel = []
        dscriptl = []
        damountl = []
        dsum = 0
        for i in d:
            dl.append(i)
            dm = max(dl)
            dn = min(dl)

            if i >= s and i <= e and e > s:
                ddate = db.child("Debit").child(i).child("Date").shallow().get().val()
                ddatel.append(ddate)

                dscript = db.child("Debit").child(i).child("Script").shallow().get().val()
                a = dscript.upper()
                dscriptl.append(a)

                damount = db.child("Debit").child(i).child("DAmount").shallow().get().val()
                damountl.append(damount)

                dsum = dsum + damount
                dcomb_list = zip(dl, ddatel, dscriptl, damountl)  # debit

            elif s == e:
                if s in i:
                    ddate = db.child("Debit").child(i).child("Date").shallow().get().val()
                    ddatel.append(ddate)

                    dscript = db.child("Debit").child(i).child("Script").shallow().get().val()
                    a = dscript.upper()
                    dscriptl.append(a)

                    damount = db.child("Debit").child(i).child("DAmount").shallow().get().val()
                    damountl.append(damount)

                    dsum = dsum + damount
                    dcomb_list = zip(dl, ddatel, dscriptl, damountl)  # debit

            elif e < dn:
                msg = "Select Valid date"
                return render(request, "accounting/report.html", {"msg": msg})

            elif e < s:
                msg = "End Date < Start Date"
                return render(request, "accounting/report.html", {"msg": msg})

            elif s > dm:
                msg = "Select Valid date"
                return render(request, "accounting/report.html", {"msg": msg})

        return render(request, "accounting/report3.html", {"comb_list": dcomb_list, "dsum": dsum})


    # credit
    elif a == "CREDIT":
        c = db.child("Credit").shallow().get().val()
        cl = []
        cdatel = []
        cscriptl = []
        camountl = []
        csum = 0
        for i in c:
            cl.append(i)
            cm = max(cl)
            cn = min(cl)

            if i >= s and i <= e and e > s:
                cdate = db.child("Credit").child(i).child("Date").shallow().get().val()
                cdatel.append(cdate)

                cscript = db.child("Credit").child(i).child("Script").shallow().get().val()
                a = cscript.upper()
                cscriptl.append(a)

                camount = db.child("Credit").child(i).child("CAmount").shallow().get().val()
                camountl.append(camount)

                csum = csum + camount
                ccomb_list = zip(cl, cdatel, cscriptl, camountl)  # credit

            elif s == e:
                if s in i:
                    cdate = db.child("Credit").child(i).child("Date").shallow().get().val()
                    cdatel.append(cdate)

                    cscript = db.child("Credit").child(i).child("Script").shallow().get().val()
                    a = cscript.upper()
                    cscriptl.append(a)

                    camount = db.child("Credit").child(i).child("CAmount").shallow().get().val()
                    camountl.append(camount)

                    csum = csum + camount
                    ccomb_list = zip(cl, cdatel, cscriptl, camountl)  # credit

            elif e < cn:
                msg = "Select Valid date"
                return render(request, "accounting/report.html", {"msg": msg})

            elif e < s:
                msg = "End Date < Start Date"
                return render(request, "accounting/report.html", {"msg": msg})

            elif s > cm:
                msg = "Select Valid date"
                return render(request, "accounting/report.html", {"msg": msg})

        return render(request, "accounting/report2.html", {"comb_list": ccomb_list, "csum": csum})



    # trading journal credit
    elif a == "TRADING JOURNAL CREDIT":
        tjc = db.child("Trading Journal Credit").shallow().get().val()
        tjcl = []
        tjcdatel = []
        tjcscriptl = []
        tjcamountl = []
        tjcsum = 0
        for i in tjc:
            tjcl.append(i)
            tjcm = max(tjcl)
            tjcn = min(tjcl)

            if i >= s and i <= e and e > s:
                tjcdate = db.child("Trading Journal Credit").child(i).child("Date").shallow().get().val()
                tjcdatel.append(tjcdate)

                tjcscript = db.child("Trading Journal Credit").child(i).child("Script").shallow().get().val()
                a = tjcscript.upper()
                tjcscriptl.append(a)

                tjcamount = db.child("Trading Journal Credit").child(i).child("tjcAmount").shallow().get().val()
                tjcamountl.append(tjcamount)

                tjcsum = tjcsum + tjcamount
                tjccomb_list = zip(tjcl, tjcdatel, tjcscriptl, tjcamountl)  # trading journal credit

            elif s == e:
                if s in i:
                    tjcdate = db.child("Trading Journal Credit").child(i).child("Date").shallow().get().val()
                    tjcdatel.append(tjcdate)

                    tjcscript = db.child("Trading Journal Credit").child(i).child("Script").shallow().get().val()
                    a = tjcscript.upper()
                    tjcscriptl.append(a)

                    tjcamount = db.child("Trading Journal Credit").child(i).child("tjcAmount").shallow().get().val()
                    tjcamountl.append(tjcamount)

                    tjcsum = tjcsum + tjcamount
                    tjccomb_list = zip(tjcl, tjcdatel, tjcscriptl, tjcamountl)  # trading journal credit

            elif e < tjcn:
                msg = "Select Valid date"
                return render(request, "accounting/report.html", {"msg": msg})



            elif e < s:
                msg = "End Date < Start Date"
                return render(request, "accounting/report.html", {"msg": msg})

            elif s > tjcm:
                msg = "Select Valid date"
                return render(request, "accounting/report.html", {"msg": msg})

        return render(request, "accounting/report4.html", {"comb_list": tjccomb_list, "tjcsum": tjcsum})



    # trading journal debit
    elif a == "TRADING JOURNAL DEBIT":
        tjd = db.child("Trading Journal Debit").shallow().get().val()
        tjdl = []
        tjddatel = []
        tjdscriptl = []
        tjdamountl = []
        tjdsum = 0

        for i in tjd:
            tjdl.append(i)
            tjdm = max(tjdl)
            tjdn = min(tjdl)

            if i >= s and i <= e and e > s:
                tjddate = db.child("Trading Journal Debit").child(i).child("Date").shallow().get().val()
                tjddatel.append(tjddate)

                tjdscript = db.child("Trading Journal Debit").child(i).child("Script").shallow().get().val()
                a = tjdscript.upper()
                tjdscriptl.append(a)

                tjdamount = db.child("Trading Journal Debit").child(i).child("tjdAmount").shallow().get().val()
                tjdamountl.append(tjdamount)

                tjdsum = tjdsum + tjdamount
                tjdcomb_list = zip(tjdl, tjddatel, tjdscriptl, tjdamountl)  # trading journal debit

            elif s == e:
                if s in i:
                    tjddate = db.child("Trading Journal Debit").child(i).child("Date").shallow().get().val()
                    tjddatel.append(tjddate)

                    tjdscript = db.child("Trading Journal Debit").child(i).child("Script").shallow().get().val()
                    a = tjdscript.upper()
                    tjdscriptl.append(a)

                    tjdamount = db.child("Trading Journal Debit").child(i).child("tjdAmount").shallow().get().val()
                    tjdamountl.append(tjdamount)

                    tjdsum = tjdsum + tjdamount
                    tjdcomb_list = zip(tjdl, tjddatel, tjdscriptl, tjdamountl)  # trading journal debit

            elif e < tjdn:
                msg = "Select Valid date"
                return render(request, "accounting/report.html", {"msg": msg})


            elif e < s:
                msg = "End Date < Start Date"
                return render(request, "accounting/report.html", {"msg": msg})

            elif s > tjdm:
                msg = "Select Valid date"
                return render(request, "accounting/report.html", {"msg": msg})

        return render(request, "accounting/report5.html", {"comb_list": tjdcomb_list, "tjdsum": tjdsum})

    # trading journal
    else:
        tj = db.child("Trading Journal").shallow().get().val()
        tjl = []
        tjdatel = []
        tjscriptl = []
        tjamountl = []
        tjsum = 0

        for i in tj:
            tjl.append(i)
            tjm = max(tjl)
            tjn = min(tjl)

            if i >= s and i <= e and e > s:
                tjdate = db.child("Trading Journal").child(i).child("Date").shallow().get().val()
                tjdatel.append(tjdate)

                tjscript = db.child("Trading Journal").child(i).child("Script").shallow().get().val()
                a = tjscript.upper()
                tjscriptl.append(a)

                tjamount = db.child("Trading Journal").child(i).child("Amount").shallow().get().val()
                tjamountl.append(tjamount)

                if tjamount > 0:
                    tjsum = tjsum + tjamount
                else:
                    tjsum = tjsum - tjamount

            elif s == e:
                if s in i:
                    tjdate = db.child("Trading Journal").child(i).child("Date").shallow().get().val()
                    tjdatel.append(tjdate)

                    tjscript = db.child("Trading Journal").child(i).child("Script").shallow().get().val()
                    a = tjscript.upper()
                    tjscriptl.append(a)

                    tjamount = db.child("Trading Journal").child(i).child("Amount").shallow().get().val()
                    tjamountl.append(tjamount)

                    if tjamount > 0:
                        tjsum = tjsum + tjamount
                    else:
                        tjsum = tjsum - tjamount

            elif e < tjn:
                msg = "Select Valid date"
                return render(request, "accounting/report.html", {"msg": msg})

            elif e < s:
                msg = "End Date < Start Date"
                return render(request, "accounting/report.html", {"msg": msg})

            elif s > tjm:
                msg = "Select Valid date"
                return render(request, "accounting/report.html", {"msg": msg})

            tjcomb_list = zip(tjl, tjdatel, tjscriptl, tjamountl)  # trading Journal

        return render(request, "accounting/report6.html", {"comb_list": tjcomb_list, "tjsum": tjsum})


def tjl(request):
    from datetime import date
    today = date.today()
    y1 = today.strftime("%d/%m/%Y")
    z = "Trading Journal Ledger"
    z1 = "Trading Journal Ledger PDF"
    mix = db.child("Mixtj").shallow().get().val()

    date = []  # all dates
    scriptl = []  # script tjcredit or tjdebit
    tjcamountl = []  # amount tjcredit
    tjdamountl = []  # amount tjdebit
    ldate = []  # display date in ledger
    amount1 = []
    pamount = []  # trading journal positive amount
    namount = []  # trading journal negative amount
    rnbl = []  # running balance for trading journal ledger
    count = []
    for i in mix:
        date.append(i)
    date.sort()
    c1 = 0

    for i in date:
        script = db.child("Mixtj").child(i).child("Script").shallow().get().val()
        tjcamount = db.child("Mixtj").child(i).child("tjcAmount").shallow().get().val()
        tjdamount = db.child("Mixtj").child(i).child("tjdAmount").shallow().get().val()
        amount = db.child("Mixtj").child(i).child("Amount").shallow().get().val()
        dat = db.child("Mixtj").child(i).child("Date").shallow().get().val()

        # script
        a = script.upper()
        scriptl.append(a)  # insert script(tj debit and tjcredit) in list

        # credit amount
        if tjcamount == None:
            tjcamountl.append("none")
        else:
            tjcamountl.append(tjcamount)

        # debit amount
        if tjdamount == None:
            tjdamountl.append("none")
        else:
            tjdamountl.append(tjdamount)

        # ldate

        ldate.append(dat)
        c1 = c1 + 1
        count.append(c1)
        date.sort()

        # trading journal amount
        if amount == None:
            amount1.append("none")
        else:
            amount1.append(amount)

    for i in amount1:
        if i == "none":
            pamount.append(i)
            namount.append(i)
        elif i < 0:
            pamount.append("none")
            namount.append(abs(i))
        else:
            pamount.append(i)
            namount.append("none")

    comb_list1 = zip(ldate, scriptl, tjcamountl, tjdamountl, pamount, namount)
    rnb = 0
    for d, s, c, d, p, n in comb_list1:
        if c != "none":
            rnb = rnb + c
            rnbl.append(rnb)
        elif d != "none":
            rnb = rnb - d
            rnbl.append(rnb)
        elif p != "none":
            rnb = rnb + p
            rnbl.append(rnb)
        elif n != "none":
            rnb = rnb - n
            rnbl.append(rnb)
        else:
            pass

    # total amount of running balance
    rn = 0
    for i in rnbl:
        rn = rn + i

    # Debit Amount Total
    dsum = 0
    dcomb = zip(tjdamountl, namount)
    for i, j in dcomb:
        if j != "none":
            if j < 0:
                dsum = dsum - j
            else:
                dsum = dsum + j
        elif i != "none":
            dsum = dsum + i

    # Credit Amount Total
    csum = 0
    ccomb = zip(tjcamountl, pamount)
    for i, j in ccomb:
        if j != "none":
            csum = csum + j
        elif i != "none":
            csum = csum + i

    l = []
    k = []
    comb_list = zip(ldate, scriptl, tjcamountl, tjdamountl, pamount, namount, rnbl)
    for ld, s, tjc, tjd, p, n, r in comb_list:
        if tjc != "none":
            k.append(tjc)
        else:
            pass
        if p != "none":
            k.append(p)
        else:
            pass
        if tjc == "none" and p == "none":
            k.append("-")
        if tjd != "none":
            l.append(tjd)
        else:
            pass
        if n != "none":
            l.append(n)
        else:
            pass
        if tjd == "none" and n == "none":
            l.append("-")

    template = get_template("accounting/invoice1.html")
    context = {
        "y": y1,
        "date": ldate,
        "count": count,
        "bill": scriptl,
        "rnbl": rnbl,
        "rn": rn,
        "csum": csum,
        "dsum": dsum,
        "l": l,
        "k": k,
        "z": z,
        "z1": z1

    }

    html = template.render(context)
    pdf = render_to_pdf("accounting/invoice1.html", context)

    return HttpResponse(pdf, content_type='application/pdf')


def vl(request):  # pdf for general ledger
    from datetime import date
    today = date.today()
    y1 = today.strftime("%d/%m/%Y")
    z = "General Ledger"
    z1 = "General Ledger PDF"
    '''
          mix = mix date
          bill = script
          date = date
          amount = tjamount(negative)
          camount = tjamount(positive)
          ccamount = credit amount
          vamount = vouchers amount
          damount = debut amount
          rnb = runnung balance
          '''

    # mix
    mix = db.child("Mix").shallow().get().val()

    mix1 = []
    for i in mix:
        mix1.append(i)
    mix1.sort()

    # bill
    bill = []

    for i in mix1:
        bill1 = db.child('Mix').child(i).child('Script').get().val()
        a = bill1.upper()
        bill.append(a)
    # bill.sort(reverse=True)

    ccamount = []
    amount = []
    camount = []

    # tjamount(negative)
    for i in mix1:
        amount1 = db.child('Mix').child(i).child('Amount').get().val()
        if amount1 != None:
            if amount1 < 0:
                camount.append("none")
                amount.append(abs(amount1))
            else:
                camount.append(amount1)
                amount.append("none")

        else:
            amount.append("none")
            camount.append("none")
    # amount.sort(reverse=True)

    # tjamount(positive)
    for i in mix1:
        amount1 = db.child('Mix').child(i).child('CAmount').get().val()
        if amount1 != None:
            ccamount.append(amount1)
        else:
            ccamount.append("none")
    # amount.sort(reverse=True)

    # Debit Amount
    damount = []
    for i in mix1:
        amount1 = db.child('Mix').child(i).child('DAmount').get().val()
        if amount1 != None:
            damount.append(amount1)
        else:
            damount.append("none")
    # amount.sort(reverse=True)

    # vouchers amount
    vamount = []
    for i in mix1:
        amount1 = db.child('Mix').child(i).child('VAmount').get().val()
        if amount1 != None:
            vamount.append(amount1)
        else:
            vamount.append("none")
    # amount.sort(reverse=True)

    # date
    date = []
    count = []
    j = 0
    for i in mix1:
        date1 = db.child('Mix').child(i).child('Date').get().val()
        j = j + 1
        count.append(j)
        date.append(date1)
    # date.sort(reverse=True)

    # runing balance
    rnb = 0
    rnbl = []

    comb_list1 = zip(mix, bill, date, amount, camount, ccamount, vamount, damount)
    for m, b, d, a, ca, cca, v, d1 in comb_list1:
        if a != "none":
            rnb = rnb - a
            rnbl.append(rnb)
        elif ca != "none":
            rnb = rnb + ca
            rnbl.append(rnb)
        elif cca != "none":
            rnb = rnb + cca
            rnbl.append(rnb)
        elif v != "none":
            rnb = rnb - v
            rnbl.append(rnb)
        elif d1 != "none":
            rnb = rnb - d1
            rnbl.append(rnb)

    # total amount of running balance
    rn = 0
    for i in rnbl:
        rn = rn + i

    # Debit Amount Total
    combsumd = zip(amount, vamount, damount)
    dsum = 0
    for i, j, k in combsumd:
        if k != "none":
            dsum = dsum + k
        elif j != "none":
            dsum = dsum + j
        elif i != "none":
            if i < 0:
                dsum = dsum - i
            else:
                dsum = dsum + i

    # Credit Amount Total

    combsumc = zip(ccamount, camount)
    csum = 0
    for i, j in combsumc:
        if j != "none":
            csum = csum + j
        elif i != "none":
            csum = csum + i

    comb_list = zip(mix, bill, date, amount, camount, ccamount, vamount, damount)
    l = []  # all debit amount
    k = []  # all credit amount

    for i, b, d, a, c, cc, v, d in comb_list:
        if a != "none":
            l.append(a)
        else:
            pass
        if v != "none":
            l.append(v)
        else:
            pass
        if d != "none":
            l.append(d)
        else:
            pass
        if a == "none" and v == "none" and d == "none":
            l.append("-")
        else:
            pass
        if c != "none":
            k.append(c)
        else:
            pass
        if cc != "none":
            k.append(cc)
        else:
            pass
        if c == "none" and cc == "none":
            k.append("-")
        else:
            pass

    template = get_template("accounting/invoice1.html")
    context = {
        "y": y1,
        "date": date,
        "bill": bill,
        "vamount": vamount,
        "damount": damount,
        "amount": amount,
        "dsum": dsum,
        "csum": csum,
        "rnbl": rnbl,
        "rn": rn,
        "ccamount": ccamount,
        "camount": camount,
        "count": count,
        "k": k,
        "l": l,
        "z": z,
        "z1": z1

    }

    html = template.render(context)
    pdf = render_to_pdf("accounting/invoice1.html", context)

    return HttpResponse(pdf, content_type='application/pdf')


def get(request):  # pdf for report
    from datetime import date
    today = date.today()
    y1 = today.strftime("%d/%m/%Y")

    a1 = a2
    s1 = s2
    e1 = e2
    if a1 == "VOUCHERS":
        z = "Vouchers Report"
        z1 = "Vouchers Report PDF"
        datel = []
        date1l = []
        scriptl = []
        amountl = []

        date = db.child("Vouchers").shallow().get().val()
        vsum = 0
        count = 0
        c = []
        for i in date:
            datel.append(i)
        datel.sort()
        for i in datel:
            if str(i) >= s1 and str(i) <= e1 and e1 > s1:
                date1 = db.child("Vouchers").child(i).child("Date").shallow().get().val()
                date1l.append(date1)
                script = db.child("Vouchers").child(i).child("Script").shallow().get().val()
                a = script.upper()
                scriptl.append(a)
                amount = db.child("Vouchers").child(i).child("VAmount").shallow().get().val()
                amountl.append(amount)

                vsum = vsum + amount
                count = count + 1
                c.append(count)


            elif s1 == e1:
                if s1 in str(i):
                    date = db.child("Vouchers").child(i).child("Date").shallow().get().val()
                    date1l.append(date)

                    script = db.child("Vouchers").child(i).child("Script").shallow().get().val()
                    a = script.upper()
                    scriptl.append(a)

                    amount = db.child("Vouchers").child(i).child("VAmount").shallow().get().val()
                    amountl.append(amount)

                    vsum = vsum + amount
                    count = count + 1
                    c.append(count)

            template = get_template("accounting/invoice.html")
            context = {
                "date": date1l,
                "script": scriptl,
                "amount": amountl,
                "total": vsum,
                "count": c,
                "y": y1,
                "z": z,
                "z1": z1
            }

        html = template.render(context)
        pdf = render_to_pdf("accounting/invoice.html", context)

        return HttpResponse(pdf, content_type='application/pdf')
    elif a1 == "DEBIT":
        z = "Debit Report"
        z1 = "Debit Report PDF"
        count = 0
        c = []
        datel = []
        date1l = []
        scriptl = []
        amountl = []

        date = db.child("Debit").shallow().get().val()
        vsum = 0
        for i in date:
            datel.append(i)
        datel.sort()
        for i in datel:
            if str(i) >= s1 and str(i) <= e1 and e1 > s1:
                date1 = db.child("Debit").child(i).child("Date").shallow().get().val()
                date1l.append(date1)
                script = db.child("Debit").child(i).child("Script").shallow().get().val()
                a = script.upper()
                scriptl.append(a)
                amount = db.child("Debit").child(i).child("DAmount").shallow().get().val()
                amountl.append(amount)

                vsum = vsum + amount
                count = count + 1
                c.append(count)


            elif s1 == e1:
                if s1 in str(i):
                    date = db.child("Debit").child(i).child("Date").shallow().get().val()
                    date1l.append(date)

                    script = db.child("Debit").child(i).child("Script").shallow().get().val()
                    a = script.upper()
                    scriptl.append(a)

                    amount = db.child("Debit").child(i).child("DAmount").shallow().get().val()
                    amountl.append(amount)

                    vsum = vsum + amount
                    count = count + 1
                    c.append(count)

            template = get_template("accounting/invoice.html")
            context = {
                "date": date1l,
                "script": scriptl,
                "amount": amountl,
                "total": vsum,
                "count": c,
                "y": y1,
                "z": z,
                "z1": z1
            }

        html = template.render(context)
        pdf = render_to_pdf("accounting/invoice.html", context)

        return HttpResponse(pdf, content_type='application/pdf')

    elif a1 == "CREDIT":
        z = "Credit Report"
        z1 = "Credit Report PDF"
        count = 0
        c = []
        datel = []
        date1l = []
        scriptl = []
        amountl = []

        date = db.child("Credit").shallow().get().val()
        vsum = 0
        for i in date:
            datel.append(i)
        datel.sort()
        for i in datel:
            if str(i) >= s1 and str(i) <= e1 and e1 > s1:
                date1 = db.child("Credit").child(i).child("Date").shallow().get().val()
                date1l.append(date1)
                script = db.child("Credit").child(i).child("Script").shallow().get().val()
                a = script.upper()
                scriptl.append(a)
                amount = db.child("Credit").child(i).child("CAmount").shallow().get().val()
                amountl.append(amount)

                vsum = vsum + amount
                count = count + 1
                c.append(count)


            elif s1 == e1:
                if s1 in str(i):
                    date = db.child("Credit").child(i).child("Date").shallow().get().val()
                    date1l.append(date)

                    script = db.child("Credit").child(i).child("Script").shallow().get().val()
                    a = script.upper()
                    scriptl.append(a)

                    amount = db.child("Credit").child(i).child("CAmount").shallow().get().val()
                    amountl.append(amount)

                    vsum = vsum + amount
                    count = count + 1
                    c.append(count)

            template = get_template("accounting/invoice.html")
            context = {
                "date": date1l,
                "script": scriptl,
                "amount": amountl,
                "total": vsum,
                "count": c,
                "y": y1,
                "z": z,
                "z1": z1
            }

        html = template.render(context)
        pdf = render_to_pdf("accounting/invoice.html", context)

        return HttpResponse(pdf, content_type='application/pdf')

    elif a1 == "TRADING JOURNAL":
        z = "Trading Journal Report"
        z1 = "Trading Journal PDF"
        count = 0
        c = []
        datel = []
        date1l = []
        scriptl = []
        amountl = []

        date = db.child("Trading Journal").shallow().get().val()
        vsum = 0
        for i in date:
            datel.append(i)
        datel.sort()
        for i in datel:
            if str(i) >= s1 and str(i) <= e1 and e1 > s1:
                date1 = db.child("Trading Journal").child(i).child("Date").shallow().get().val()
                date1l.append(date1)
                script = db.child("Trading Journal").child(i).child("Script").shallow().get().val()
                a = script.upper()
                scriptl.append(a)
                amount = db.child("Trading Journal").child(i).child("Amount").shallow().get().val()
                amountl.append(amount)

                if amount < 0:
                    vsum = vsum - amount
                else:
                    vsum = vsum + amount
                count = count + 1
                c.append(count)


            elif s1 == e1:
                if s1 in str(i):
                    date = db.child("Trading Journal").child(i).child("Date").shallow().get().val()
                    date1l.append(date)

                    script = db.child("Trading Journal").child(i).child("Script").shallow().get().val()
                    a = script.upper()
                    scriptl.append(a)

                    amount = db.child("Trading Journal").child(i).child("Amount").shallow().get().val()
                    amountl.append(amount)

                    if amount < 0:
                        vsum = vsum - amount
                    else:
                        vsum = vsum + amount

                    count = count + 1
                    c.append(count)

            template = get_template("accounting/invoice.html")
            context = {
                "date": date1l,
                "script": scriptl,
                "amount": amountl,
                "total": vsum,
                "count": c,
                "y": y1,
                "z": z,
                "z1": z1
            }

        html = template.render(context)
        pdf = render_to_pdf("accounting/invoice.html", context)

        return HttpResponse(pdf, content_type='application/pdf')

    elif a1 == "TRADING JOURNAL CREDIT":
        z = "Trading Journal Credit Report"
        z1 = "Trading Journal Credit PDF"
        count = 0
        c = []
        datel = []
        date1l = []
        scriptl = []
        amountl = []

        date = db.child("Trading Journal Credit").shallow().get().val()
        vsum = 0
        for i in date:
            datel.append(i)
        datel.sort()
        for i in datel:
            if str(i) >= s1 and str(i) <= e1 and e1 > s1:
                date1 = db.child("Trading Journal Credit").child(i).child("Date").shallow().get().val()
                date1l.append(date1)
                script = db.child("Trading Journal Credit").child(i).child("Script").shallow().get().val()
                a = script.upper()
                scriptl.append(a)
                amount = db.child("Trading Journal Credit").child(i).child("tjcAmount").shallow().get().val()
                amountl.append(amount)

                vsum = vsum + amount
                count = count + 1
                c.append(count)


            elif s1 == e1:
                if s1 in str(i):
                    date = db.child("Trading Journal Credit").child(i).child("Date").shallow().get().val()
                    date1l.append(date)

                    script = db.child("Trading Journal Credit").child(i).child("Script").shallow().get().val()
                    a = script.upper()
                    scriptl.append(a)

                    amount = db.child("Trading Journal Credit").child(i).child("tjcAmount").shallow().get().val()
                    amountl.append(amount)

                    vsum = vsum + amount
                    count = count + 1
                    c.append(count)

            template = get_template("accounting/invoice.html")
            context = {
                "date": date1l,
                "script": scriptl,
                "amount": amountl,
                "total": vsum,
                "count": c,
                "y": y1,
                "z": z,
                "z1": z1
            }

        html = template.render(context)
        pdf = render_to_pdf("accounting/invoice.html", context)

        return HttpResponse(pdf, content_type='application/pdf')
    elif a1 == "TRADING JOURNAL DEBIT":
        z = "Trading Journal Debit Report"
        z1 = "Trading Journal Debit PDF"
        count = 0
        c = []
        datel = []
        date1l = []
        scriptl = []
        amountl = []

        date = db.child("Trading Journal Debit").shallow().get().val()
        vsum = 0
        for i in date:
            datel.append(i)
        datel.sort()
        for i in datel:
            if str(i) >= s1 and str(i) <= e1 and e1 > s1:
                date1 = db.child("Trading Journal Debit").child(i).child("Date").shallow().get().val()
                date1l.append(date1)
                script = db.child("Trading Journal Debit").child(i).child("Script").shallow().get().val()
                a = script.upper()
                scriptl.append(a)
                amount = db.child("Trading Journal Debit").child(i).child("tjdAmount").shallow().get().val()
                amountl.append(amount)

                vsum = vsum + amount
                count = count + 1
                c.append(count)


            elif s1 == e1:
                if s1 in str(i):
                    date = db.child("Trading Journal Debit").child(i).child("Date").shallow().get().val()
                    date1l.append(date)

                    script = db.child("Trading Journal Debit").child(i).child("Script").shallow().get().val()
                    a = script.upper()
                    scriptl.append(a)

                    amount = db.child("Trading Journal Debit").child(i).child("tjdAmount").shallow().get().val()
                    amountl.append(amount)

                    vsum = vsum + amount
                    count = count + 1
                    c.append(count)

            template = get_template("accounting/invoice.html")
            context = {
                "date": date1l,
                "script": scriptl,
                "amount": amountl,
                "total": vsum,
                "count": c,
                "y": y1,
                "z": z,
                "z1": z1
            }

        html = template.render(context)
        pdf = render_to_pdf("accounting/invoice.html", context)

        return HttpResponse(pdf, content_type='application/pdf')


def tjentry(request):
    email = request.POST.get('uname')
    passw = request.POST.get('pass')

    try:
        user = authe.sign_in_with_email_and_password(email, passw)
    except:
        return render(request, "accounting/tjloginerror.html")
    # print(user['idToken'])
    # session_id = user['idToken']
    # request.session['uid'] = str(session_id)

    return render(request, "accounting/tjentry.html")


def credit(request):
    email = request.POST.get('uname')
    passw = request.POST.get('pass')

    try:
        user = authe.sign_in_with_email_and_password(email, passw)
    except:
        return render(request, "accounting/creditloginerror.html")

    return render(request, "accounting/credit.html")


def tjcredit(request):
    email = request.POST.get('uname')
    passw = request.POST.get('pass')

    try:
        user = authe.sign_in_with_email_and_password(email, passw)
    except:
        return render(request, "accounting/tjcreditloginerror.html")

    return render(request, "accounting/tjcredit.html")


def debit(request):
    email = request.POST.get('uname')
    passw = request.POST.get('pass')

    try:
        user = authe.sign_in_with_email_and_password(email, passw)
    except:
        return render(request, "accounting/debitloginerror.html")

    return render(request, "accounting/debit.html")


def tjdebit(request):
    email = request.POST.get('uname')
    passw = request.POST.get('pass')

    try:
        user = authe.sign_in_with_email_and_password(email, passw)
    except:
        return render(request, "accounting/tjdebitloginerror.html")

    return render(request, "accounting/tjdebit.html")


def report(request):
    email = request.POST.get('uname')
    passw = request.POST.get('pass')

    try:
        user = authe.sign_in_with_email_and_password(email, passw)
    except:
        return render(request, "accounting/reportloginerror.html")

    return render(request, "accounting/report.html")


# insert data in database

def post_ve(request):
    import time
    from datetime import datetime, timezone
    import pytz

    # create time zone
    tz = pytz.timezone('Asia/Kolkata')

    # get the current datatime
    time_now = datetime.now(timezone.utc).astimezone(tz)

    # convert time_now into miliseconds
    millis = int(time.mktime(time_now.timetuple()))
    print("milis-:" + str(millis))

    date = request.POST.get('date')
    d = str(date)
    m = str(millis)
    dm = d + '-' + m
    print(dm)
    bill = request.POST.get('bill')

    amount = request.POST.get('amount')
    details = request.POST.get('details')

    data = {
        "Date": date,
        "Script": bill,
        "Script1": "VOUCHERS",
        "VAmount": int(amount),
        "Details": details

    }
    # t1 = str(date)+str(millis)
    # print("t1",t1)
    if db.child('Vouchers').child(dm).set(data):
        if db.child('Mix').child(dm).set(data):
            message = "Data Insert Successfully"
            return render(request, "accounting/idn.html", {"msg": message})


    else:
        pass
    return render(request, "accounting/vouchersentry.html")


def post_tj(request):
    from datetime import datetime
    import time
    from datetime import datetime, timezone
    import pytz

    # create time zone
    tz = pytz.timezone('Asia/Kolkata')

    # get the current datatime
    time_now = datetime.now(timezone.utc).astimezone(tz)

    # convert time_now into miliseconds
    millis = int(time.mktime(time_now.timetuple()))
    print("milis-:" + str(millis))

    date1 = request.POST.get('date')
    d = str(date1)
    m = str(millis)
    dm = d + '-' + m
    print(dm)

    # date1 = request.POST.get('date')
    time1 = request.POST.get('time')
    script = request.POST.get('script')
    script.capitalize()
    quantity = request.POST.get('quantity')
    bs = request.POST.get('bs')
    entry = request.POST.get('entry')
    sl = request.POST.get('sl')
    tsl = request.POST.get('tsl')
    exit = request.POST.get('exit')
    pl = request.POST.get('pl')
    plt = request.POST.get('plt')
    '''
    d = date1
    print("Date" + str(d))
    t = datetime.now().strftime("%H:%M:%S:%p")
    # t = time1
    print("Time" + str(t))
    '''
    data = {
        "Date": date1,
        "Time": time1,
        "Script": script,
        "Script1": "TRADING JOURNAL",
        "Quantity": quantity,
        "Buy&Sell": bs,
        "Entry": entry,
        "StopLoss": sl,
        "Traling StopLoss": tsl,
        "Exit": exit,
        "Amount": int(pl),
        "Profite&Loss after Tax": plt,
    }

    if db.child('Trading Journal').child(dm).set(data):
        if db.child('Mixtj').child(dm).set(data):
            if db.child('Mix').child(dm).set(data):
                message = "Data Insert Successfully"
                return render(request, "accounting/tjentry.html", {"msg": message})
    else:
        pass
    return render(request, "accounting/tjentry.html")


def post_debit(request):
    import time
    from datetime import datetime, timezone
    import pytz
    # create time zone
    tz = pytz.timezone('Asia/Kolkata')

    # get the current datatime
    time_now = datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))
    date = request.POST.get('date')
    amount = request.POST.get('amount')

    data = {
        "Date": date,
        "DAmount": int(amount),
        "Script": "Debit",
        "Script1": "DEBIT"

    }
    d = str(date)
    m = str(millis)
    dm = d + '-' + m
    print(dm)
    if db.child('Debit').child(dm).set(data):
        if db.child('Mix').child(dm).set(data):
            message = "Data Insert Successfully"
            return render(request, "accounting/debit.html", {'msg': message})
    else:
        pass
    return render(request, "accounting/debit.html")


def post_credit(request):
    import time
    from datetime import datetime, timezone
    import pytz

    # create time zone
    tz = pytz.timezone('Asia/Kolkata')

    # get the current datatime
    time_now = datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))
    date = request.POST.get('date')
    amount = request.POST.get('amount')

    data = {
        "Date": date,
        "CAmount": int(amount),
        "Script": "Credit",
        "Script1": "CREDIT"

    }
    d = str(date)
    m = str(millis)
    dm = d + '-' + m
    print(dm)
    if db.child('Credit').child(dm).set(data):
        if db.child('Mix').child(dm).set(data):
            message = "Data Insert Successfully"
            return render(request, "accounting/credit.html", {'msg': message})
        else:
            pass
        return render(request, "accounting/credit.html")

    else:
        pass
    return render(request, "accounting/credit.html")


def tj_post_credit(request):
    import time
    from datetime import datetime, timezone
    import pytz

    # create time zone
    tz = pytz.timezone('Asia/Kolkata')

    # get the current datatime
    time_now = datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))
    date = request.POST.get('date')
    amount = request.POST.get('amount')

    data = {
        "Date": date,
        "tjcAmount": int(amount),
        "Script": "Trading Journal Credit",
        "Script1": "TRADING JOURNAL CREDIT"

    }
    d = str(date)
    m = str(millis)
    dm = d + '-' + m
    print(dm)
    if db.child('Trading Journal Credit').child(dm).set(data):
        if db.child('Mixtj').child(dm).set(data):
            message = "Data Insert Successfully"
            return render(request, "accounting/tjcredit.html", {'msg': message})
        else:
            pass
        return render(request, "accounting/tjcredit.html")

    else:
        pass
    return render(request, "accounting/tjcredit.html")


def tj_post_debit(request):
    import time
    from datetime import datetime, timezone
    import pytz

    # create time zone
    tz = pytz.timezone('Asia/Kolkata')

    # get the current datatime
    time_now = datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))
    date = request.POST.get('date')
    amount = request.POST.get('amount')

    data = {
        "Date": date,
        "tjdAmount": int(amount),
        "Script": "Trading Journal Debit",
        "Script1": "TRADING JOURNAL DEBIT"
    }
    d = str(date)
    m = str(millis)
    dm = d + '-' + m
    print(dm)
    if db.child('Trading Journal Debit').child(dm).set(data):
        if db.child('Mixtj').child(dm).set(data):
            message = "Data Insert Successfully"
            return render(request, "accounting/tjdebit.html", {'msg': message})
        else:
            pass
        return render(request, "accounting/tjdebit.html")

    else:
        pass
    return render(request, "accounting/tjdebit.html")
