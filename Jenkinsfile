node ('git') {
    properties([
        parameters([
            string(name: 'docker_registry', defaultValue: '')
        ])
    ])

    stage ('checkout') {
        checkout scm
    }

    stage ('build-image') {
        def imgName = 'config-manager'
        def registry = params.docker_registry

        def img = docker.build("${registry}/${imgName}")

        docker.withRegistry("https://${registry}", 'hitc-docker-registry') {
            img.push()
        }
    }
}
