import boto3
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from project import settings


class UploadImage(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, format=None):
        image = request.FILES['image']
        s3 = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        bucket = s3.Bucket(settings.AWS_S3_BUCKET_NAME)
        string_key = f"public/{image.name}"
        bucket.put_object(Key=string_key,
                          Body=image, ACL='public-read')
        public_url = f"https://s3-{settings.AWS_S3_REGION_NAME}.amazonaws.com/{settings.AWS_S3_BUCKET_NAME}/{string_key}"

        content = {
            'image_name': image.name,
            'image_size': image.size,
            'public_url': public_url,
        }

        return Response(content)
