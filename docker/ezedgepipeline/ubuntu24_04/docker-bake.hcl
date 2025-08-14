variable "TAG" {
 default = "latest"   
}

variable "HOST_UID" {
    default = 1000 # Fallback value
}

variable "HOST_GID" {
    default = 1000 # Fallback value
}

variable "REGISTRY" {
    default = "visagir"
}

group "default" {
    targets = ["r_apt", "r_minifi_cpp", "r_ezedgepipeline"]
    args = {
        HOST_UID = "${HOST_UID}"
        HOST_GID = "${HOST_GID}"
    }
    platforms = ["linux/amd64"]
}

##
# VISAGIR Ez Edge Pipeline
##
target "r_apt" {
    network = "host"
    context = "r_10_apt"
    tags = ["${REGISTRY}/r_apt:${TAG}"]
}

target "r_minifi_cpp" {
    network = "host"
    context = "r_15_minifi_cpp"
    contexts = {
        r_apt = "target:r_apt"
    }
    tags = ["${REGISTRY}/r_minifi_cpp:${TAG}"]
}

target "r_ezedgepipeline" {
    context = "r_20_entries"
    contexts = {
        r_minifi_cpp = "target:r_minifi_cpp"
        r_apt = "target:r_apt"
    }
    tags = ["${REGISTRY}/r_ezedgepipeline:${TAG}"]
}
