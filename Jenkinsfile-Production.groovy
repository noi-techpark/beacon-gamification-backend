pipeline {
    agent any

    environment {
        DOCKER_PROJECT_NAME = "gamification-api"
        DOCKER_IMAGE = '755952719952.dkr.ecr.eu-west-1.amazonaws.com/gamification-api'
        DOCKER_TAG = "prod-$BUILD_NUMBER"

        DJANGO_DEBUG = 'False'
        SECRET_KEY = credentials('beacon-gamification-api-prod-secret-key')
        S3_ACCESS_KEY_ID = credentials('beacon-gamification-api-prod-aws-access-key-id')
        S3_SECRET_ACCESS_KEY = credentials('beacon-gamification-api-prod-aws-secret-access-key')
        S3_REGION = 'eu-west-1'
        S3_BUCKET_NAME = 'prod-gamification-api'
    }

    stages {
        stage('Configure') {
            steps {
                sh """
                    rm -f .env
                    cp .env.example .env
                    echo 'COMPOSE_PROJECT_NAME=${DOCKER_PROJECT_NAME}' >> .env
                    echo 'DOCKER_IMAGE=${DOCKER_IMAGE}' >> .env
                    echo 'DOCKER_TAG=${DOCKER_TAG}' >> .env

                    echo 'DJANGO_DEBUG=${DJANGO_DEBUG}' >> .env
                    echo 'SECRET_KEY=${SECRET_KEY}' >> .env
                    echo 'AWS_ACCESS_KEY_ID=${S3_ACCESS_KEY_ID}' >> .env
                    echo 'AWS_SECRET_ACCESS_KEY=${S3_SECRET_ACCESS_KEY}' >> .env
                    echo 'S3_REGION=${S3_REGION}' >> .env
                    echo 'S3_BUCKET_NAME=${S3_BUCKET_NAME}' >> .env
                """
            }
        }

        stage('Test') {
            steps {
                sh '''
                    docker-compose --no-ansi build --pull --build-arg JENKINS_USER_ID=$(id -u jenkins) --build-arg JENKINS_GROUP_ID=$(id -g jenkins)
                    docker-compose --no-ansi run --rm --no-deps -u $(id -u jenkins):$(id -g jenkins) app python --version
                '''
            }
        }
        stage('Build') {
            steps {
                sh '''
                    aws ecr get-login --region eu-west-1 --no-include-email | bash
                    docker-compose --no-ansi -f docker-compose.build.yml build --pull
                    docker-compose --no-ansi -f docker-compose.build.yml push
                '''
            }
        }
        stage('Deploy') {
            steps {
               sshagent(['jenkins-ssh-key']) {
                    sh """
                        ansible-galaxy install --force -r ansible/requirements.yml
                        ansible-playbook --limit=prod ansible/deploy.yml --extra-vars "build_number=${BUILD_NUMBER}"
                    """
                }
            }
        }
    }
}
