_mkfile_dir := $(dir $(abspath $(word $(words $(MAKEFILE_LIST)),$(MAKEFILE_LIST))))
_mkfile_dir := $(_mkfile_dir:/=)

_app_dir := $(abspath ${_mkfile_dir}/../../../..)
_cm_dir := $(abspath ${_mkfile_dir}/../..)

_config_tool := ${_app_dir}/lib/config.py

deployment_name :=

_key_chain := ${deployment_name} cm

-validate-deployment-name:
	[ -n "${deployment_name}" ] || ( echo 'ERROR: deployment_name must be provided' >&2; exit 1 )

_tmp_dir := /tmp/ansible/ubuntu-focal/${deployment_name}
_inventory_file := ${_tmp_dir}/digitalocean.inventory
_config_file := ${_tmp_dir}/secrets-config.yml

-create-inventory-file: -validate-deployment-name
	mkdir -p $$(dirname "${_inventory_file}") && \
	remote_ips="$$(${_config_tool} --key-chain "${_key_chain}" --ips)" envsubst \
		< ${_cm_dir}/inventory.template \
		> ${_inventory_file}

-create-config-file: -validate-deployment-name
	${_config_tool} --key-chain "${_key_chain}" --output-file="${_config_file}"

debug:
	make -- -create-config-file

run: -create-inventory-file -create-config-file
	cd "${_mkfile_dir}" && \
	ansible-playbook \
		--inventory-file "${_inventory_file}" \
    --extra-vars "cm_dir=${_cm_dir}" \
    --extra-vars "@${_config_file}" \
		${_mkfile_dir}/playbook.yml

# # do_reset_and_migrate=yes: run on one server first, then
# #   do_reset_and_migrate=no on the rest of the servers
# cm-ubuntu-focal-digitalocean-run: -cm-ubuntu-focal-digitalocean-build-inventory
# 	cd "${_mkfile_dir}" && \
# 	ansible-playbook \
# 		--inventory-file "${_inventory_file}" \
# 		--extra-vars secrets_dir="${_secrets_dir}" \
# 		--extra-vars do_reset_and_migrate='yes' \
#     --extra-vars "@${_mkfile_dir}/../../vars.yml" \
#     --extra-vars "cm_dir=${_cm_dir}" \
#     --extra-vars "@${_app_dir}/db/postgres.yml" \
#     --extra-vars '{"tls_container":${tls}}' \
#     --extra-vars "fetched_tls_files_dir=${fetched_tls_files_dir}" \
#     --extra-vars '@${domain_config_file}' \
# 		${_mkfile_dir}/playbook.yml

.PHONY: debug -validate-deployment-name -create-inventory-file -create-config-file
