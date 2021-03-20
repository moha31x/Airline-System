"""This scripts takes a web request and returns a web response."""
from io import BytesIO
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from xhtml2pdf import pisa
from .models import Passenger, Flight



# Create your views here.

def login_staff(request):
    """Method to perform staff login details."""
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                if user.user_type == 1:
                    login(request, user)
                    return redirect('view_flights')
                else:
                    return render(
                        request, 'staff_login.html',
                        {'error_message': 'Invalid flight staff credentials'}
                    )
            else:
                return render(
                    request, 'staff_login.html', {
                        'error_message': 'Your account has been disabled'
                    }
                )
        else:
            return render(
                request, 'staff_login.html', {
                    'error_message': 'Invalid login'
                }
            )
    return render(request, 'staff_login.html')


def home(request):
    return render(request, 'home.html')


def staff_home(request, flight_no):
    """Method to render homepage."""
    # staff = get_object_or_404(Staff, peek=peek)
    data = Passenger.filter(flight_no=flight_no)
    flight = Flight.filter(flight_no=flight_no)
    return render(
        request, 'staff_home.html', {
            'passengers': data, 'flight': flight, 'flight_no': flight_no
        }
    )

    
def view_flights(request):
    """Method to render all flights."""
    data = Flight.all()
    return render(request, 'view_flights.html', {'flights': data})


def self_check_in(peek):
    """Method to perform self check-in"""
    passenger = get_object_or_404(Passenger, peek=peek)
    passenger.checked_in_status = True
    passenger.save()
    return redirect('passenger_home', peek=passenger.peek)


def search_by_source(request):
    """Method to render origins."""
    if request.method == "POST":
        source = request.POST['source']
        if source:
            data = Flight.filter(source=source)
            return render(request, 'view_flights.html', {'flights': data})
        else:
            return redirect('view_flights')       
    else:
        return redirect('view_flights')


def search_by_destination(request):
    """Method to render destinations."""
    if request.method == "POST":
        destination = request.POST['destination']
        if destination:
            data = Flight.filter(destination=destination)
            return render(request, 'view_flights.html', {'flights': data})
        else:
            return redirect('view_flights')
    else:
        return redirect('view_flights')


def view_available_flights(request):
    """Method to render available flights."""
    if request.method == "POST":
        source = request.POST['source']
        destination = request.POST['destination']
        if source and destination:
            flights = Flight.filter(source=source, destination=destination)
            if flights:
                return render(request, 'home.html', {'flights': flights})
            else:
                return render(
                    request, 'home.html', {
                        'error_message_flight': "No flights found"
                    }
                )
        else:
            return redirect('home')
    else:
        return redirect('home')


def book_flight(request, peek):
    """Method to perform flight booking."""
    if request.method == "POST":
        flight = Flight.get(flight_no=peek)
        user = request.user
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        nationality = request.POST['nationality']
        gender = request.POST['gender']
        ppno = request.POST['ppno']
        dob = request.POST['dob']
        pnr = str(flight.flight_no) + str(flight.destination)
        passenger = Passenger(
            pnr=pnr, first_name=first_name, last_name=last_name,
            nationality=nationality, flight_no=flight, gender=gender,
            ppno=ppno, dob=dob, booked_by=user
        )
        passenger.save()
        passenger.pnr = str(
            flight.flight_no
        ) + str(
            flight.destination_code
        ) + str(
            passenger.peek
        )
        passenger.save()
        flight.no_of_seats -= 1
        flight.save()
        return redirect('view_flights')
    else:
        return render(request, 'book_flight.html', {'flight_no': peek})


def passenger_home(request, peek):
    passenger = Passenger.get(peek=peek)
    return render(request, 'passenger_home.html', {'passenger': passenger})


def view_booking(request):
    if request.method == "POST":  # view existing booking
        pnr = request.POST['pnr']
        try:
            passenger = Passenger.get(pnr=pnr)
        except Passenger.DoesNotExist:
            passenger = None
        if passenger:
            passenger = get_object_or_404(Passenger, pnr=pnr)
            return render(
                request, 'passenger_home.html', {'passenger': passenger}
            )
        else:
            return render(
                request, 'home.html', {
                    'error_message_booking': 'No booking found'
                }
            )


def staff_check_in(peek):
    """method to perform passenger check in"""
    passenger = get_object_or_404(Passenger, peek=peek)
    passenger.checked_in_status = True
    passenger.save()
    return redirect('staff_home', flight_no=passenger.flight_no.flight_no)


def render_to_pdf(template_src, context_dict: dict):
    template = loader.get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    else:
        return None


# Opens up page as PDF
def pdf_view(flight_no):
    passengers = Passenger.filter(flight_no=flight_no)

    data = {
        "airline": "Air Starline",
        "passengers": passengers
    }

    pdf = render_to_pdf('flights/pdf_template.html', data)
    return HttpResponse(pdf, content_type='application/pdf')


def pdf_invoice(peek):
    """method to print passenger invoice"""
    passenger = Passenger.get(peek=peek)
    data = {
        "airline": "Air Starline",
        "passenger": passenger
    }

    pdf = render_to_pdf('flights/pdf_invoice.html', data)
    return HttpResponse(pdf, content_type='application/pdf')


# Automaticly downloads to PDF file
def pdf_download(flight_no):
    """method to perform pdf downloads"""
    passengers = Passenger.filter(flight_no=flight_no)

    data = {
        "airline": "Air Starline",
        "passengers": passengers
        }

    pdf = render_to_pdf('flights/pdf_template.html', data)

    response = HttpResponse(pdf, content_type='application/pdf')
    filename = "Flight_Report_%s.pdf" % ("12341231")
    content = "attachment; filename=%s" % (filename)
    response['Content-Disposition'] = content
    return response


def dl_invoice(peek):
    """method for printing client invoices."""
    passenger = Passenger.get(peek=peek)
    data = {
        "airline": "Air Starline",
        "passenger": passenger
    }

    pdf = render_to_pdf('flights/pdf_invoice.html', data)

    response = HttpResponse(pdf, content_type='application/pdf')
    filename = "Invoice_%s.pdf" % ("12341")
    content = "attachment; filename=%s" % (filename)
    response['Content-Disposition'] = content
    return response
