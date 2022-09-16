###################################
# first run the playbook on the "older pre-upgrade os"
FROM ubuntu:20.04 as old
WORKDIR /etc/ansible/roles/role_under_test

RUN apt-get -qq update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
  software-properties-common

# get newer ansible than in default ubuntu
RUN apt-add-repository -y ppa:ansible/ansible

RUN apt-get -qq update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
  ansible

# Install Ansible inventory file.
RUN mkdir -p /etc/ansible
RUN echo "[local]\nlocalhost ansible_connection=local" > /etc/ansible/hosts

COPY . /etc/ansible/roles/role_under_test

# run the playbook
RUN ansible-playbook tests/test.yml


##############################
# copy the virualenv over to the new "upgraded" os and try to run again
# as if we have done an upgrade without clearing the virtualenv
FROM ubuntu:22.04 as new
COPY --from=old /usr/local/lib/docker/virtualenv /usr/local/lib/docker/virtualenv
WORKDIR /etc/ansible/roles/role_under_test

RUN apt-get -qq update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
  software-properties-common gpg-agent

# get newer ansible than in default ubuntu
RUN apt-add-repository -y ppa:ansible/ansible

RUN apt-get -qq update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
  ansible

# Install Ansible inventory file.
RUN mkdir -p /etc/ansible
RUN echo "[local]\nlocalhost ansible_connection=local" > /etc/ansible/hosts

COPY . /etc/ansible/roles/role_under_test

# run the playbook
RUN ansible-playbook tests/test.yml
