from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, LoginSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from .models import User, SpamNumber, Contact
from rest_framework import status
from .serializers import SpamNumberSerializer


@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Function to mark as spam

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_as_spam(request):
    if 'phone_number' not in request.data:
        return Response({'message': 'Phone number is required.'}, status=status.HTTP_400_BAD_REQUEST)

    phone_number = request.data.get('phone_number')

    if SpamNumber.objects.filter(phone_number=phone_number, reported_by=request.user).exists():
        return Response({'message': 'You have already marked this number as spam.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        spam_number = SpamNumber.objects.create(
            phone_number=phone_number,
            reported_by=request.user
        )

        is_spam = SpamNumber.check_and_update_spam_status(phone_number)

        if is_spam:
            return Response({'message': 'Number marked as spam and flagged as spam due to multiple reports.'},
                            status=status.HTTP_201_CREATED)

        return Response({'message': 'Number marked as spam.'}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#Function to search by name

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_by_name(request):
    query = request.query_params.get('query', None)
    if not query:
        return Response({'message': 'Query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

    users_by_name_start = User.objects.filter(name__startswith=query)

    users_by_name_contain = User.objects.filter(name__icontains=query).exclude(name__startswith=query)

    users_by_name = users_by_name_start | users_by_name_contain

    search_results = []

    if not users_by_name.exists():
        return Response({'message': 'No user found'}, status=status.HTTP_404_NOT_FOUND)

    for user in users_by_name:
        spam = SpamNumber.objects.filter(phone_number=user.phone_number).first()
        spam_status = spam.spam_status if spam else False

        email = None
        if Contact.objects.filter(user=request.user, contact_number=user.phone_number).exists():
            email = user.email

        search_results.append({
            'name': user.name,
            'phone_number': user.phone_number,
            'spam_likelihood': 'Spam' if spam_status else 'Not Spam',
            'email': email
        })

    return Response(search_results, status=status.HTTP_200_OK)

#Function to search by phone number

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_by_phone_number(request):
    query = request.query_params.get('query', None)
    if not query:
        return Response({'message': 'Query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

    search_results = []

    user_by_phone = User.objects.filter(phone_number=query).first()

    if user_by_phone:
        spam = SpamNumber.objects.filter(phone_number=user_by_phone.phone_number).first()
        spam_status = spam.spam_status if spam else False

        email = None
        if Contact.objects.filter(user=request.user, contact_number=user_by_phone.phone_number).exists():
            email = user_by_phone.email

        search_results.append({
            'name': user_by_phone.name,
            'phone_number': user_by_phone.phone_number,
            'spam_likelihood': 'Spam' if spam_status else 'Not Spam',
            'email': email
        })

        return Response(search_results, status=status.HTTP_200_OK)

    else:
        users_by_number = User.objects.filter(phone_number=query)

        if not users_by_number.exists():
            return Response({'message': 'No user found'}, status=status.HTTP_404_NOT_FOUND)

        for user in users_by_number:
            spam = SpamNumber.objects.filter(phone_number=user.phone_number).first()
            spam_status = spam.spam_status if spam else False

            email = None
            if Contact.objects.filter(user=request.user, contact_number=user.phone_number).exists():
                email = user.email

            search_results.append({
                'name': user.name,
                'phone_number': user.phone_number,
                'spam_likelihood': 'Spam' if spam_status else 'Not Spam',
                'email': email
            })

    return Response(search_results, status=status.HTTP_200_OK)



#Function to list down contacts for a particular user

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_contacts(request):
    contacts = Contact.objects.filter(user=request.user)

    contact_list = []
    for contact in contacts:
        contact_list.append({
            'contact_name': contact.contact_name,
            'contact_number': contact.contact_number
        })

    if contact_list:
        return Response({'contacts': contact_list}, status=200)
    else:
        return Response({'message': 'No contacts found.'}, status=404)


#Function to add contacts

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_contact(request):

    contact_name = request.data.get('contact_name')
    contact_number = request.data.get('contact_number')

    if not contact_name or not contact_number:
        return Response({'message': 'Both contact name and contact number are required.'}, status=status.HTTP_400_BAD_REQUEST)

    contact = Contact.objects.create(
        user=request.user,
        contact_name=contact_name,
        contact_number=contact_number
    )

    return Response({
        'message': 'Contact added successfully.',
        'contact_name': contact.contact_name,
        'contact_number': contact.contact_number
    }, status=status.HTTP_201_CREATED)