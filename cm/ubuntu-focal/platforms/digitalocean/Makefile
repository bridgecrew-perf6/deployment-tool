deployment_name :=

_mkfile_dir := $(dir $(abspath $(word $(words $(MAKEFILE_LIST)),$(MAKEFILE_LIST))))
_mkfile_dir := $(_mkfile_dir:/=)

_app_dir := $(abspath ${_mkfile_dir}/../../../..)
_cm_dir := $(abspath ${_mkfile_dir}/../..)

_section := cm

_lib_dir = ${_app_dir}/lib
_config_tool := ${_lib_dir}/config.py --deployment-name "${deployment_name}" --section "${_section}"

-validate-deployment-name:
	[ -n "${deployment_name}" ] || ( echo 'ERROR: deployment_name must be provided' >&2; exit 1 )

_tmp_dir := /tmp/ansible/ubuntu-focal/${deployment_name}
_inventory_file := ${_tmp_dir}/digitalocean.inventory
_config_file := ${_tmp_dir}/secrets-config.yml

-create-inventory-file: -validate-deployment-name
	mkdir -p $$(dirname "${_inventory_file}") && \
	remote_ips="$$(${_config_tool} --ips)" envsubst \
		< ${_cm_dir}/inventory.template \
		> ${_inventory_file}

-create-config-file: -validate-deployment-name
	${_config_tool} --output-file="${_config_file}"

_cert_files_dir := $$(${_config_tool} --key-chain cert_files_dir)
-setup-certs:
	if [ -n "${_cert_files_dir}" ]; then \
		mkdir -p "$$(dirname "${_cert_files_dir}")"; \
	fi

run: -create-inventory-file -create-config-file -setup-certs
	cd "${_mkfile_dir}" && \
	ansible-playbook \
		--inventory-file "${_inventory_file}" \
		--extra-vars "app_name=${deployment_name}" \
    --extra-vars "cm_dir=${_cm_dir}" \
    --extra-vars "@${_config_file}" \
    --extra-vars "@${_cm_dir}/vars.yml" \
		${_mkfile_dir}/playbook.yml && \
		${_lib_dir}/extract-tls.py --deployment-name "${deployment_name}"

.PHONY: -validate-deployment-name -create-inventory-file -create-config-file -setup-certs run
