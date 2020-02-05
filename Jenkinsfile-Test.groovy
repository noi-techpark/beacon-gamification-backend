pipeline {
    agent any

    environment {
        AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')
		DOCKER_PROJECT_NAME = "gamification-api"
		DOCKER_SERVER_IP = "63.33.73.203"
        DOCKER_SERVER_DIRECTORY = "/var/docker/gamification-api"
		DOCKER_IMAGE = '755952719952.dkr.ecr.eu-west-1.amazonaws.com/gamification-api'
		DOCKER_TAG = "test-$BUILD_NUMBER"

		DJANGO_DEBUG = 'False'
		SECRET_KEY = credentials('gamification-api-test-secrect-key')
		AWS_ACCESS_KEY_ID = credentials('gamification-api-test-aws-access-key-id')
		AWS_SECRET_ACCESS_KEY = credentials('gamification-api-test-aws-secrect-access-key')
		S3_REGION = 'eu-west-1'
		S3_BUCKET_NAME = 'test-gamification-api'
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
					echo 'AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}' >> .env
					echo 'AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}' >> .env
					echo 'S3_REGION=${S3_REGION}' >> .env
					echo 'S3_BUCKET_NAME=${S3_BUCKET_NAME}' >> .env
				"""
            }
        }

        stage('Test') {
            steps {
				sh '''
					docker-compose --no-ansi build --pull --build-arg JENKINS_USER_ID=$(id -u jenkins) --build-arg JENKINS_GROUP_ID=$(id -g jenkins)
					docker-compose --no-ansi run --rm --no-deps -u $(id -u jenkins):$(id -g jenkins) app "python --version"
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
					    ssh -o StrictHostKeyChecking=no ${DOCKER_SERVER_IP} bash -euc "'
							mkdir -p ${DOCKER_SERVER_DIRECTORY}
							mkdir -p ${DOCKER_SERVER_DIRECTORY}/shared
							touch ${DOCKER_SERVER_DIRECTORY}/shared/db.sqlite3
							ls -1t ${DOCKER_SERVER_DIRECTORY}/releases/ | tail -n +10 | grep -v `readlink -f ${DOCKER_SERVER_DIRECTORY}/current | xargs basename --` -- | xargs -r printf \"${DOCKER_SERVER_DIRECTORY}/releases/%s\\n\" | xargs -r rm -rf --
							mkdir -p ${DOCKER_SERVER_DIRECTORY}/releases/${BUILD_NUMBER}
							ln -sfn ${DOCKER_SERVER_DIRECTORY}/shared/db.sqlite3 ${DOCKER_SERVER_DIRECTORY}/releases/${BUILD_NUMBER}/db.sqlite3
						'"

						scp -o StrictHostKeyChecking=no docker-compose.run.yml ${DOCKER_SERVER_IP}:${DOCKER_SERVER_DIRECTORY}/releases/${BUILD_NUMBER}/docker-compose.yml
						scp -o StrictHostKeyChecking=no .env ${DOCKER_SERVER_IP}:${DOCKER_SERVER_DIRECTORY}/releases/${BUILD_NUMBER}/.env

						ssh -o StrictHostKeyChecking=no ${DOCKER_SERVER_IP} bash -euc "'
							AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" aws ecr get-login --region eu-west-1 --no-include-email | bash
							cd ${DOCKER_SERVER_DIRECTORY}/releases/${BUILD_NUMBER} && docker-compose --no-ansi pull
							[ -d \"${DOCKER_SERVER_DIRECTORY}/current\" ] && (cd ${DOCKER_SERVER_DIRECTORY}/current && docker-compose --no-ansi down) || true
							ln -sfn ${DOCKER_SERVER_DIRECTORY}/releases/${BUILD_NUMBER} ${DOCKER_SERVER_DIRECTORY}/current
							cd ${DOCKER_SERVER_DIRECTORY}/current && docker-compose --no-ansi up --detach
						'"
					"""
                }
            }
        }
    }
}
