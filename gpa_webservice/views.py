from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect
from gpa_webservice.forms import SignUpForm
from gpa_webservice.models import User
from gpa_webservice.utils import Util, token_generator


class HomeView(generic.TemplateView):
    template_name = 'base.html'


class SignUpView(generic.CreateView):
    """ SignUp view """

    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

    def send_activation_email(self, request, user):
        """ sends email confirmation email """

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)

        domain = get_current_site(request).domain
        schema = request.is_secure() and "https" or "http"

        link = reverse('user_activation', kwargs={'uidb64': uidb64, 'token': token})
        url = '{}://{}{}'.format(schema, domain, link)

        payload = {
            'receiver': user.email,
            'email_body': {
                'username': user.username,
                'email_body': 'Verify your email to finish signing up for RapidReady',
                'link': url,
                'link_text': 'Verify Your Email',
                'email_reason': "You're receiving this email because you signed up in {}".format(domain),
                'site_name': domain
            },
            'email_subject': 'Verify your Email',
        }

        Util.send_email(payload)
        messages.success(request, 'Please Confirm your email to complete registration.')

    def get(self, request, *args, **kwargs):
        """ Prevents authenticated user accessing registration path """

        if request.user.is_authenticated:
            return redirect('index')
        return super(SignUpView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        """ Handles valid form """

        form = self.form_class(self.request.POST)

        user = form.save(commit=False)
        user.is_active = False
        user.save()

        self.send_activation_email(self.request, user)

        return render(self.request, 'registration/confirm_email.html', {'email': user.email})

    def post(self, request, *args, **kwargs):
        """ Handles existing inactive user registration attempt """

        form = self.form_class(self.request.POST)

        if User.objects.filter(email=request.POST['email']).exists():
            user = User.objects.get(email=request.POST['email'])
            if not user.is_active:
                self.send_activation_email(request, user)

                return render(self.request, 'registration/confirm_email.html', {'email': user.email})
        # if no record found pass to form_valid
        return super().post(request, *args, **kwargs)

