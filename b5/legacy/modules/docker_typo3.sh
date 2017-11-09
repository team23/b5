#!/usr/bin/env bash

b5:module_load docker_composer

docker_typo3:db_populate() {
    # Import all sql files from _db_import folder
    lockfile="./_db_import/.import_finished"
    test -d ./_db_import || return
    test -f $lockfile && {
        echo -e "\n${B5_FONT_RED}Tables have already been imported. To reimport delete ${lockfile}. ${B5_FONT_RESTORE}"
    }

    statement="SET names 'utf8'; USE docker;"
    tables_added=""
    for fn in ./_db_import/*.sql; do
        file="${DOCKER_COMPOSER_PATH}/${fn}"
        table="$(basename $fn .sql)"
        tables_added="${tables_added} ${table}"
        statement="${statement}TRUNCATE TABLE $table; ALTER TABLE $table AUTO_INCREMENT = 1; SOURCE $file;"
    done;
    touch $lockfile
    echo -e "\n${B5_FONT_GREEN}Tables imported: ${tables_added}${B5_FONT_RESTORE}"
    docker_composer:runbin sh -c "echo \"$statement\" | typo3cms database:import"

}

task:typo3() {
    docker_composer:runbin typo3 "$@"
}

task:typo3cms() {
    docker_composer:runbin typo3cms "$@"
}

task:setup() {
    task:typo3cms install:setup --non-interactive \
        --database-user-name="docker" \
        --database-user-password="docker" \
        --database-host-name="db" \
        --database-port="3306" \
        --database-name="docker" \
        --admin-user-name="team23" \
        --admin-password="testen23" \
        --use-existing-database \
        --site-name="${DOCKER_PROJECT_NAME}"
    task:typo3cms extension:activate tstemplate,about,belog,beuser,context_help,fluid_styled_content,form,func,impexp,info,info_pagetsconfig,lowlevel,opendocs,recycler,reports,rsaauth,rte_ckeditor,setup,sys_action,sys_note,t3editor,taskcenter,version,viewpage,wizard_crpages,wizard_sortpages
    task:typo3cms upgrade:all
    docker_typo3:db_populate
}


task:itc() {
    docker_composer:runbin touch ../web/typo3conf/ENABLE_INSTALL_TOOL && \
    echo -e "\n${B5_FONT_GREEN}Touched typo3conf/ENABLE_INSTALL_TOOL${B5_FONT_RESTORE}"
}

task:itr() {
    docker_composer:runbin rm -f ../web/typo3conf/ENABLE_INSTALL_TOOL && \
    echo -e "\n${B5_FONT_GREEN}Removed typo3conf/ENABLE_INSTALL_TOOL${B5_FONT_RESTORE}"
}

task:cc() {
    task:typo3cms cache:flush
}