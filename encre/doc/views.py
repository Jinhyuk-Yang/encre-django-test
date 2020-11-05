from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer

from core import models

def get_login_user_email(request):
    """JWT를 통해 로그인한 유저의 이메일 주소를 획득"""
    return VerifyJSONWebTokenSerializer().validate({"token": request.auth})['user']

class MyIndicesView(GenericAPIView):
    """작성한 문서의 ID 조회"""
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        try:
            # Verify user from JWT token
            email = get_login_user_email(request)
            writer_id = models.User.objects.get(email=email).id
            # Find documents
            doc_queryset = models.Document.objects.filter(writer__id=writer_id)
            return Response(
                {
                    'msg': 'Id list of my documents',
                    'indices': [doc.id for doc in doc_queryset]
                }, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'internal_error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DocView(GenericAPIView):
    """문서 추가 / 문서의 목록 조회"""
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        try:
            doc_queryset = models.Document.objects.all()
            return Response(
                {
                    'msg': 'Id list of total documents',
                    'indices': [doc.id for doc in doc_queryset]
                }, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'internal_error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        try:
            # Verify user from JWT token
            email = get_login_user_email(request)
            writer = models.User.objects.get(email=email)

            if len(set(request.data.keys()).symmetric_difference({'head', 'body'})) > 0:
                return Response(
                    {'validation_error': 'Invalid data.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            models.Document.objects.create(
                head=request.data['head'],
                body=request.data['body'],
                writer=writer
            )
            return Response({'msg': 'OK'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'internal_error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DocIndexView(GenericAPIView):
    """문서 일기/수정/삭제"""
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request, doc_id):
        try:
            doc = models.Document.objects.get(id=doc_id)
            status_code = status.HTTP_200_OK
            response = {
                'msg': 'Information of a document.',
                'head': doc.head,
                'body': doc.body,
                'writer': doc.writer.email
            }

        except Exception:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'validation_error': 'Document does not exists',
            }
        return Response(response, status=status_code)

    def put(self, request, doc_id):
        if not {'head', 'body'}.issuperset(set(request.data.keys())):
            return Response(
                {'validation_error': 'Invalid data.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            # Verify user from JWT token
            email = get_login_user_email(request)
            writer_id = models.User.objects.get(email=email).id

            doc = models.Document.objects.get(id=doc_id)
            if doc.writer is None or doc.writer.id != writer_id:
                return Response(
                    {'validation_error': 'You are not writer.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except Exception:
            return Response(
                {'validation_error': 'Cannot find a document.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        is_updated = False
        if request.data.get('head', None) is not None:
            doc.head = request.data['head']
            is_updated = True
        if request.data.get('body', None) is not None:
            doc.body = request.data['body']
            is_updated = True
        
        if is_updated:
            doc.save()

        return Response({'msg': 'OK'}, status=status.HTTP_200_OK)
    
    def delete(self, request, doc_id):
        try:
            # Verify user from JWT token
            email = get_login_user_email(request)
            writer_id = models.User.objects.get(email=email).id

            doc = models.Document.objects.get(id=doc_id)
            if doc.writer is None or doc.writer.id != writer_id:
                return Response(
                    {'validation_error': 'You are not writer.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except Exception:
            return Response(
                {'validation_error': 'Cannot find a document.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        doc.delete()
        
        return Response({'msg': 'OK'}, status=status.HTTP_200_OK)
