pipeline {
    environment {
        nexusDockerRegistryUrl = "docker-production.bnc.ca"
        deploymentAgent = "5677/snowflake-ci-agent:latest"
    }

    options {
        disableConcurrentBuilds()
    }

    agent any

    stages {
        stage("Initialize") {
            steps {
                script {
                    /* Uses the Jenkins folders tree to determine the various parameters. */
                    (applicationId, environment) = env.JOB_NAME.split("/")[0..1]

                    /* Loads the Tool stack config file created by the enroller to get tool stack IDs. */
                    configFileProvider([configFile(fileId: "tool-stacks", targetLocation: "tool-stacks.json")]) {
                        toolStacksConfig = readJSON file: "tool-stacks.json"
                        toolStackId = toolStacksConfig.active
                        artifactManagementCredentialStoreEntry = "${toolStackId}.artifact-management"
                    }

                    /* Loads the secret manager (vault) configuration. */
                    configFileProvider([configFile(fileId: "${toolStackId}.secret-management", targetLocation: "secret-management.json")]) {
                        secretManagementJson = readJSON file: "secret-management.json"
                    }
                }
            }
        }

        stage("Flake8 Validation") {
            steps {
                script {
                    docker.withRegistry("https://${nexusDockerRegistryUrl}", artifactManagementCredentialStoreEntry) {
                        sh "docker rmi ${nexusDockerRegistryUrl}/${deploymentAgent} --force || true"

                        docker.image(deploymentAgent).inside() {
                            sh """
                            flake8 python-cookie-cutter
                            """
                        }
                    }
                }
            }
        }

        stage("Unit Tests") {
            steps {
                script {
                    docker.withRegistry("https://${nexusDockerRegistryUrl}", artifactManagementCredentialStoreEntry) {
                        docker.image(deploymentAgent).inside() {
                            sh """
                            pytest python-cookie-cutter -vv
                            """
                        }
                    }
                }
            }
        }

        stage("Integration Testing") {
            steps {
                echo 'Place Holder'
            }
        }
    }
}