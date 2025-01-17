*** Settings ***
Resource  resource.robot
Library   AppLibrary

*** Test Cases ***
Add Reading Tip With Valid Title And Link
    Input Add Reading Tip Command
    Input    Tirakirja
    Input    https://www.cs.helsinki.fi/u/ahslaaks/tirakirja/
    Input See All Reading Tips Command
    Input Exit Command
    Run Application
    Output Should Contain    New Reading Tip added!
    Output Should Contain    Id: 1, Title: Tirakirja, URL: https://www.cs.helsinki.fi/u/ahslaaks/tirakirja/