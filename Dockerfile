# syntax=docker/dockerfile:1

FROM ubuntu:22.04

# Update packages and install dependencies
RUN apt update -y && apt upgrade -y
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa

# Installing Python
RUN apt install python3 python3-pip -y

# Installing Node.js
RUN apt install nodejs npm -y

# Installing SQLite3
RUN apt install sqlite3 -y

# Installing SSH
RUN apt install openssh-server -y

# Disallow password-based SSH logins
RUN sed -E -i 's|^#?(PasswordAuthentication)\s.*|\1 no|' /etc/ssh/sshd_config && \
    if ! grep '^PasswordAuthentication\s' /etc/ssh/sshd_config; then echo 'PasswordAuthentication no' >> /etc/ssh/sshd_config; fi

# Create SSH directory and authorized_keys file
RUN mkdir /root/.ssh
RUN touch /root/.ssh/authorized_keys

# Add your public key (replace with your actual public key)
RUN echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC37HFQ3ZO0bAOyeVCu+0S/u+oV5uf4r82+aZGX3YnSKY6tc38dowHHi5UayLiUvCu3QHnI6+r56+0jKYXpCOtWT8K58Xjhv/iMRmI1hbmB7t/VzsQ0C+bjzzF/g87V0nP4PjpegCyPVgLxAB/a5IhF2NhplEqRsNiig+wzpt4nnjxPDZHmL5MOkZyZEv7r0J9oVIGV7dX9uUIaoHGy3E9diyV6U2fB0POmIwnUseSuRcrtUUzAZIcfIaQUBO1RUCNlAckSzKL8mWsoyxzUdrxQzcx6T55aDkgju5Gt345a6iAKiJ7gTnjANEmEednwBXdsLSfQXotGKlGXlGvCljtqd0Omnmj1+ADnAJBrcJTBVAy859p+nmtmKtThClXI5/XKrr/qYqp72Jgs/eZWLzekzNTthSvLRLZucD7w9nzrPC6D3Axr2tNgVRWZ++l2PcOoYoimi6epaSLR3QfhtyvY+M+UTyvLpZwP96tfKDmXxHCnHUcVr75ZyMRqhysMWsU= isaac@FlyingKomputer" >> /root/.ssh/authorized_keys

# Set permissions for SSH directory and authorized_keys file
RUN chmod 700 /root/.ssh
RUN chmod 600 /root/.ssh/authorized_keys

# Starting SSH service
RUN service ssh start

# Change directory
WORKDIR /hydrolab

# NPM requirements
COPY package-lock.json .
COPY package.json .
RUN npm install

# Python requirements
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

# Copying all
COPY . .

# Setting up database
RUN if [ ! -f *.db ]; then python3 db_init.py; fi

# Compiling CSS
RUN npm run create-css

# Compiling translations
RUN pybabel compile -f -d app/translations

# Expose port for SSH and the application
EXPOSE 22 5000

# Environment variable
ENV PRODUCTION=True

# Starting SSH and the application
CMD service ssh start && python3 app.py
