node ('git') {
    stage ('checkout'{ {
        git url: 'git@git.hitc:config_manager.git'
    }

    stage ('build-image') {
        def imgName = 'config-manager'
        def registry = 'docker-registry.hendrikx-itc.nl:5000'

        def img = docker.build("${registry}/${imgName}")

        docker.withRegistry("https://${registry}", 'hitc-docker-registry') {
            img.push()
        }
    }
}
