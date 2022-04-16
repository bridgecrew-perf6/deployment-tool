_mkfile_dir := $(dir $(abspath $(word $(words $(MAKEFILE_LIST)),$(MAKEFILE_LIST))))
_mkfile_dir := $(_mkfile_dir:/=)

_app_dir := $(abspath ${_mkfile_dir}/../../../..)
_cm_dir := $(abspath ${_mkfile_dir}/../..)

_config_tool := ${_app_dir}/lib/config.py

deployment_name :=

-validate-deployment-name:
	[ -n "${deployment_name}" ] || ( echo 'ERROR: deployment_name must be provided' >&2; exit 1 )

_tmp_dir := /tmp/ansible/ubuntu-focal/${deployment_name}
_inventory_file := ${_tmp_dir}/digitalocean.inventory
_config_file := ${_tmp_dir}/secrets-config.yml

-create-inventory-file: -validate-deployment-name
	mkdir -p $$(dirname "${_inventory_file}") && \
	remote_ips="$$(${_config_tool} --key-chain '${deployment_name} cm' --ips)" envsubst \
		< ${_cm_dir}/inventory.template \
		> ${_inventory_file}

debug:
	make -- -create-inventory-file

run: -create-inventory-file
	cd "${_mkfile_dir}" && \
	ansible-playbook \
		--inventory-file "${_inventory_file}" \
		${_mkfile_dir}/playbook.yml

.PHONY: debug -validate-deployment-name -create-inventory-file run
