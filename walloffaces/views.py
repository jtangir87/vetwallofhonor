from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import FormView, CreateView, DetailView
from bootstrap_datepicker_plus import DatePickerInput
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.template.loader import get_template
from django.core.mail import send_mail
from django.conf import settings

from .models import Veteran
from .forms import BioForm, DonateForm, RemembranceForm


import stripe

stripe_pub_key = settings.STRIPE_PUBLISHABLE_KEY
stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.


def home_view(request):
    vets_list = Veteran.objects.filter(approved=True)
    page = request.GET.get("page", 1)

    paginator = Paginator(vets_list, 24)

    try:
        vets = paginator.page(page)
    except PageNotAnInteger:
        vets = paginator.page(1)
    except EmptyPage:
        vets = paginator.page(paginator.num_pages)

    donate_form = DonateForm()
    context = {"vets": vets, "donate_form": donate_form,
               "stripe_pub_key": stripe_pub_key}

    return render(request, "home.html", context)


class VeteranCreate(SuccessMessageMixin, CreateView):
    model = Veteran
    fields = ("name", "hometown", "county", "dob", "doc", "branch",
              "rank", "status", "country", "image", "bio")
    template_name = "bio_form.html"
    success_url = "/"
    success_message = "Veteran submitted successfully!"

    def get_form(self):
        form = super().get_form()
        form.fields['dob'].widget = DatePickerInput()
        form.fields['doc'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        ## EMAIL ELEANOR ##
        template = get_template("vet_bio_submit.txt")
        context = {}
        content = template.render(context)
        send_mail(
            "New Veteran Bio Submitted",
            content,
            "Vet Wall Bios <donotreply@elevatedwebsystems.com>",
            ["mail@coldwarhistory.org"],
            fail_silently=False,
        )

        return super().form_valid(form)

# class VeteranForm(FormView):
#     form_class = BioForm
#     template_name = "bio_form.html"
#     success_url = "/"


class VeteranDetail(DetailView):
    model = Veteran
    template_name = "veteran_detail.html"
    context_object_name = "vet"

    def get_context_data(self, **kwargs):
        context = super(VeteranDetail, self).get_context_data(**kwargs)
        context["form"] = RemembranceForm(initial={"veteran": self.object.id})
        return context


def remembrance_form(request, vet_id):
    if request.method == "POST":
        form = RemembranceForm(request.POST or None)
        if form.is_valid():
            form.save()
            ## EMAIL ELEANOR ##
            template = get_template("remembrance_received.txt")
            context = {
            }
            content = template.render(context)
            send_mail(
                "New Remembrance",
                content,
                "Vet Wall <donotreply@elevatedwebsystems.com>",
                ["mail@coldwarhistory.org"],
                fail_silently=False,
            )

            messages.success(
                request, "Success! Thank you for submitting your remembrance! Once approved, it will display on this wall forever")

            return HttpResponseRedirect(reverse("vet_detail", kwargs={"pk": vet_id}))

        else:
            print(form.errors)
            form = RemembranceForm(request.POST)
            errors = form.errors
            vet = Veteran.objects.filter(id=vet_id).first()
            context = {
                "errors": errors,
                "form": form,
                "vet": vet,
            }
            return render(request, "veteran_detail.html", context)


def donation(request):
    if request.method == "POST":
        form = DonateForm(request.POST or None)
        if form.is_valid():
            try:
                customer = stripe.Customer.create(
                    email=form.cleaned_data["email"],
                    name=form.cleaned_data["name"],
                    phone=form.cleaned_data["phone"],
                    source=request.POST["stripeToken"],
                )
            except stripe.error.CardError as e:
                # Since it's a decline, stripe.error.CardError will be caught
                body = e.json_body
                err = body["error"]
                stripe_error = err["message"]

                context = {
                    "stripe_pub_key": stripe_pub_key,
                    "form": DonateForm(request.POST),
                    "stripe_error": stripe_error,
                }
                return render(request, "donate_error.html", context)
            amount = form.cleaned_data["amount"]
            context = {"customer_id": customer.id, "amount": amount}
            return render(request, "donation_confirmation.html", context)
        else:
            errors = form.errors
            context = {
                "stripe_pub_key": stripe_pub_key,
                "form": DonateForm(request.POST),
                "errors": errors,
            }

        return render(request, "donate_error.html", context)


def confirm_donation(request):
    if request.method == "POST":
        customer_id = request.POST.get("customer_id")
        stripe_amount = int(request.POST.get("amount")) * 100

        customer = stripe.Customer.retrieve(customer_id)
        charge = stripe.Charge.create(
            customer=customer,
            amount=stripe_amount,
            currency="usd",
            description="Donation",
        )

        ## EMAIL ELEANOR ##
        template = get_template("donation_received.txt")
        context = {
            "name": customer.name,
            "phone": customer.phone,
            "email": customer.email,
            "amount": request.POST.get("amount"),
        }
        content = template.render(context)
        send_mail(
            "New Donation Received",
            content,
            "Donations <donotreply@elevatedwebsystems.com>",
            ["mail@coldwarhistory.org"],
            fail_silently=False,
        )

        ## EMAIL DONOR ##
        template = get_template("donation_received_thank_you.txt")
        context = {
            "name": customer.name,
            "amount": request.POST.get("amount"),
        }
        content = template.render(context)
        send_mail(
            "Thank You For Your Donation",
            content,
            "Donations <mail@coldwarhistory.org>",
            [customer.email],
            fail_silently=False,
        )

        return render(request, "thank_you.html")


def contact_us_form(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        message = request.POST.get("message")

        template = get_template("contact_us.txt")
        context = {
            "name": name,
            "phone": phone,
            "email": email,
            "message": message,
        }
        content = template.render(context)
        send_mail(
            "New Contact Us Submitted",
            content,
            "Veterans Wall of Honor<website@elevatedwebsystems.com>",
            ["mail@coldwarhistory.org"],
            fail_silently=False,
        )
        messages.success(request, "Success! Thank you for contacting us!")

    return redirect(reverse("home"))


def search_results(request):
    q = request.GET.get("q")

    vets_list = Veteran.objects.filter(approved=True, name__icontains=q)
    page = request.GET.get("page", 1)

    paginator = Paginator(vets_list, 24)

    try:
        vets = paginator.page(page)
    except PageNotAnInteger:
        vets = paginator.page(1)
    except EmptyPage:
        vets = paginator.page(paginator.num_pages)

    donate_form = DonateForm()
    context = {"vets": vets, "q": q, "results": vets_list.count()}

    return render(request, "search_results.html", context)
