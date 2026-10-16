
pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        timeout(time: 30, unit: 'MINUTES')
    }

    environment {
        COMPOSE_PROJECT_NAME = 'finance_app'
        COMPOSE_FILE = 'docker-compose.yaml'
        FRONTEND_URL = 'http://host.docker.internal:3001/'
        BACKEND_URL = 'http://host.docker.internal:8003/'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo "Building Finance_app from ${env.BRANCH_NAME ?: 'master'}"
            }
        }

        stage('Validate Configuration') {
            steps {
                sh '''
                    set -eu
                    test -f "$COMPOSE_FILE"
                    test -f backend/Dockerfile
                    test -f frontend/Dockerfile
                    test -f sql/Dockerfile

                    docker compose \
                      -p "$COMPOSE_PROJECT_NAME" \
                      -f "$COMPOSE_FILE" config -q

                    echo "Compose configuration is valid."
                '''
            }
        }

        stage('Backend Tests') {
            steps {
                sh '''
                    set -eu

                    if [ -d backend/tests ] && \
                       find backend/tests -type f \
                         \\( -name 'test_*.py' -o -name '*_test.py' \\) \
                         | grep -q .; then

                        docker compose \
                          -p "$COMPOSE_PROJECT_NAME" \
                          -f "$COMPOSE_FILE" build backend

                        docker compose \
                          -p "$COMPOSE_PROJECT_NAME" \
                          -f "$COMPOSE_FILE" run \
                          --rm --no-deps backend \
                          python -m pytest tests -q
                    else
                        echo "No pytest test files found; skipping tests."
                    fi
                '''
            }
        }

        stage('Build Images') {
            steps {
                sh '''
                    set -eu
                    docker compose \
                      -p "$COMPOSE_PROJECT_NAME" \
                      -f "$COMPOSE_FILE" build
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    set -eu

                    # Preserve the existing database volume.
                    docker compose \
                      -p "$COMPOSE_PROJECT_NAME" \
                      -f "$COMPOSE_FILE" \
                      up -d --remove-orphans

                    docker compose \
                      -p "$COMPOSE_PROJECT_NAME" \
                      -f "$COMPOSE_FILE" ps
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    set -eu

                    # Allow services time to start.
                    attempt=0
                    until curl -fsS "$FRONTEND_URL" -o /dev/null; do
                        attempt=$((attempt + 1))

                        if [ "$attempt" -ge 18 ]; then
                            echo "Frontend health check failed."
                            docker compose \
                              -p "$COMPOSE_PROJECT_NAME" \
                              -f "$COMPOSE_FILE" logs --tail=100
                            exit 1
                        fi

                        sleep 5
                    done

                    echo "Frontend HTTP check passed."

                    docker compose \
                      -p "$COMPOSE_PROJECT_NAME" \
                      -f "$COMPOSE_FILE" ps
                '''
            }
        }
    }

    post {
        success {
            echo 'Finance_app CI/CD pipeline completed successfully.'
            echo 'Frontend: http://localhost:3001'
            echo 'Backend:  http://localhost:8003'
        }

        failure {
            echo 'Finance_app pipeline failed. Review the stage logs.'
            sh '''
                docker compose \
                  -p finance_app \
                  -f docker-compose.yaml \
                  ps || true
            '''
        }

        always {
            echo 'Finance_app pipeline execution finished.'
        }
    }
}
