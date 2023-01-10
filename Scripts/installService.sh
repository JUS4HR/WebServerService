#!/usr/bin/env bash

scriptDir=$(dirname "$(realpath "$0")")
echo "$scriptDir"
serviceFile="../Service/webServer.service"
serviceFileTemp="../Service/temp.service"
serviceFileDestSystem="/etc/systemd/system/webServer.service"
serviceFileDestUser="$HOME/.config/systemd/user/webServer.service"

function _askWhether(){
    while true; do
        read -p "$1 ([Y]/n) " yn
        case $yn in
            [Yy][Ee][Ss]|[Yy]|"" ) return 0;;
            [Nn][Oo]|[Nn] ) return 1;;
            *) echo "Please answer yes or no.";;
        esac
    done
}

function _askForDir(){
    read -p "$1" dir
    # if starts with ~, replace it with $HOME
    if [[ $dir == ~* ]]; then
        dir="${HOME}${dir:1}"
    fi
    dirTreVal="$dir"
}

# ask for selecting a conda env
# if conda is command
if [ -x "$(command -v conda)" ]; then
    echo "Conda found."
    if _askWhether "Do you want to use conda?"; then
        condaEnvs=$(conda env list | grep -v "^#" | awk '{print $1}')
        echo "Select a conda environment from vailable conda environments for the server to run on:"
        select condaEnv in $condaEnvs; do
            if [ -n "$condaEnv" ]; then
                echo "$condaEnv selected"
                selectedCondaEnv="$condaEnv"
                break
            else
                echo "Invalid selection"
            fi
        done
    fi
fi

if [ -z "$selectedCondaEnv" ]; then
    if _askWhether "Do you want to use venv?"; then
        while true ; do
            _askForDir "Enter the path to the venv directory: "
            if [ -f "$dirTreVal/bin/activate" ]; then
                echo "venv found"
                selectedVenv=$(realpath "$dirTreVal/bin/activate")
                break
            else
                echo "venv not found, try again"
            fi
        done

    fi
fi 

# the launching command
mainPyPath=$(realpath "$scriptDir/../App/main.py")
if [ -n "$selectedCondaEnv" ]; then
    launchCommand="conda run -n $condaEnv python $mainPyPath"
    # fix Failed to locate executable conda
    launchCommand="source $(conda info --base)/etc/profile.d/conda.sh; $launchCommand"
elif [ -n "$selectedVenv" ]; then
    launchCommand="source $selectedVenv; python $mainPyPath" 
else
    launchCommand="python $mainPyPath"
fi
launchCommand="cd $(dirname "$scriptDir"); $launchCommand" 
launchCommand="bash -c '$launchCommand'"

cd "$scriptDir" || exit 1

substitutionPrefix="{{"
substitutionSuffix="}}"

# replace the launchCommand in the service file
cp "$serviceFile" "$serviceFileTemp"
stringToReplace=$substitutionPrefix"launchCommand"$substitutionSuffix
sed -i "s!$stringToReplace!$launchCommand!g" "$serviceFileTemp"

if _askWhether "Install Service for user? (For conda environment only works for user)"; then
    installForUser="true"
    # check if logincctl linger is enabled
    if ! loginctl show-user "$(whoami)" | grep -q "Linger=yes"; then
        echo "Linger is not enabled for user $(whoami)."
        if _askWhether "Do you want to enable it?"; then
            loginctl enable-linger "$(whoami)"
        fi
    fi
    if [ ! -d "$(dirname "$serviceFileDestUser")" ]; then
        mkdir -p "$(dirname "$serviceFileDestUser")"
    fi
    cp "$serviceFileTemp" "$serviceFileDestUser"
    systemctl --user daemon-reload
else
    echo "Password might be required for installing the service for system."
    sudo cp "$serviceFileTemp" "$serviceFileDestSystem"
    sudo systemctl daemon-reload
fi

rm "$serviceFileTemp"

echo
echo -e "\e[32mService installed\e[0m"
if [ -n "$installForUser" ]; then
    echo "To start the service, run:"
    echo "systemctl --user start webServer.service"
    echo "To enable the service, run:"
    echo "systemctl --user enable webServer.service"
else
    echo "To start the service, run:"
    echo "sudo systemctl start webServer.service"
    echo "To enable the service, run:"
    echo "sudo systemctl enable webServer.service"
fi
