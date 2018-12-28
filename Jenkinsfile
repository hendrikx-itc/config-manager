node ('git') {
    stage ('checkout') {
        checkout scm
    }

    stage ('build-image') {
        def imgName = 'config-manager'

        def img = docker.build("${docker_registry}/${imgName}")

        docker.withRegistry("https://${docker_registry}", 'hitc-docker-registry') {
            img.push()
        }
    }
}
