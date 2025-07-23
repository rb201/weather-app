#!/bin/bash

# TODO: usage()

cd /opt

# List of all available tools in this script
list_of_tools=(
    install_ansible
    install_argo_cli
    install_aws_cli
    install_drone_cli
    install_helm
    install_kubectl
    install_kubeseal
    install_kustomize
    install_terraform
)

install_ansible() {
    echo "Installing Ansible"
    echo ""
    pip install ansible
}


install_argo_cli() {
    echo "Installing Argo CLI"
    echo ""
    curl -sSL -o argocd https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
    sudo install -m 555 argocd-linux-amd64 /usr/local/bin/argocd
    echo ""
    argo version
}


install_aws_cli() {
    echo "installing AWSCLI"
    echo ""
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    sudo ./aws/install -i /usr/local/bin
    echo ""
    aws --version
}


install_drone_cli() {
    echo "Installing Drone CLI"
    echo ""
    curl -L https://github.com/harness/drone-cli/releases/latest/download/drone_linux_amd64.tar.gz | tar zx
    sudo install -t /usr/local/bin drone
    echo ""
    drone -version
}


install_helm() {
    echo "Installing Helm"
    echo ""
    curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
    chmod 700 get_helm.sh
    ./get_helm.sh
    echo ""
    helm version  
}


install_kubectl() {
    echo "Installing Kubectl"
    echo ""
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
    echo ""
    kubectl version --client
}


install_kubeseal() {
    echo "Installing Kubeseal"
    echo ""
    curl -OL "https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.30.0/kubeseal-0.30.0-linux-amd64.tar.gz"
    tar -xvzf kubeseal-0.30.0-linux-amd64.tar.gz kubeseal
    sudo install -m 755 kubeseal /usr/local/bin/kubeseal
    echo ""
    kubeseal --version
}


install_kustomize() {
    echo "Installing Kustomize"
    echo ""
    curl -s "https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh"  | bash
    echo ""
    kustomize version
}


install_terraform() {
    echo "Installing Terraform"
    echo ""
    wget https://releases.hashicorp.com/terraform/1.12.2/terraform_1.12.2_linux_amd64.zip
    unzip terraform_1.12.2_linux_amd64.zip
    sudo install -m 555 terraform /usr/local/bin/terraform
    echo ""
    terraform --version
}


install_all_tools() {
    for tool in "${list_of_tools[@]}"; do
        $tool
    done
}


install_selected_tools() {
    for tool in "${tools_to_install[@]}"; do
        $tool
    done
}

# Tools to install if `all` not selected
declare -a tools_to_install

while [ $# -gt 0 ]; do
    case $1 in
        all)
            ALL="true"
            break
            ;;
        argo)
            tools_to_install+=(install_argo_cli)
            shift
            ;;
        ansible)
            tools_to_install+=(install_ansible)
            shift
            ;;
        aws | awscli)
            tools_to_install+=(install_aws_cli)
            shift
            ;;
        drone)
            tools_to_install+=(install_drone_cli)
            shift
            ;;
        helm)
            tools_to_install+=(install_heml)
            shift
            ;;
        kubectl)
            tools_to_install+=(install_kubectl)
            shift
            ;;
        kubeseal)
            tools_to_install+=(install_kubeseal)
            shift
            ;;
        kustomize)
            tools_to_install+=(install_kustomize)
            shift
            ;;
        terraform)
            tools_to_install+=(install_terraform)
            shift
            ;;
        *)
            echo "Invalid option: $1"
            shift
            ;;
    esac
done

if [[ $ALL == "true" ]]; then
    echo "Installing all tools"
    install_all_tools
else
    if [ "${#tools_to_install[@]}" -eq 0 ]; then
        echo "No tools chosen for installation"
        exit 0
    else
        echo "Installing selected tools"
        install_selected_tools
    fi
fi