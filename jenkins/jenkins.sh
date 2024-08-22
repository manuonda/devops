#!/bin/bash
if [ "$EUID" -ne 0 ]; then
  echo "Este script debe ser ejecutado como root"
  exit 1
else 
  echo "Este script se esta ejecutando como root"
fi



echo "instalacion jenkins"
wget -O /usr/share/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc]" \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null


apt-get update -qq
echo " $(date) Se inicia la instalacion"
apt-get install curl openjdk-17-jre ca-certificates lsb-release gnupq jenkins -y

echo "# $(date) restart jenkins"
systemctl restart jenkins


echo "# $(date) Install complete"
echo "Username : Admin"
echo "Password :$(cat /var/lib/jenkins/secrets/initialAdminPassword)"
