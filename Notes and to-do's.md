- Selection of the appropriate schema using the header data of a GAEB xml file (schemaLocation)
  - <GAEB xmlns="http://www.gaeb.de/GAEB_DA_XML/DA82/3.3">
    <GAEBInfo>
        <Version>3.3</Version>
        <VersDate>2021-05</VersDate>
    </GAEBInfo>
    ...
    <Award>
        <DP>82</DP>
        ...
    </Award>
    </GAEB>
        
- Calling the script validate_gaeb.py via the command line and passing the XML file to be checked as an argument 
