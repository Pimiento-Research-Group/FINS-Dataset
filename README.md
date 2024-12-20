# FINS - A global dataset of fossil sharks, rays and skates from the Cretaceous to the Quaternary

This repository contains the code and data for the analyses presented in the manuscript:

**"FINS - A global dataset of fossil sharks, rays and skates from the Cretaceous to the Quaternary"**  
**Kristína Kocáková<sup>1*</sup>, Jaime A. Villafaña<sup>2</sup>, Amanda Gardiner<sup>1,3</sup>, Jürgen Pollerspöck<sup>4</sup>, Nicolas Straube<sup>5</sup>, Gregor H. Mathes<sup>1,6</sup>, Catalina Pimiento<sup>1,7</sup>**  

<sup>1</sup>Department of Paleontology, University of Zurich, Zurich, Switzerland <br />
<sup>2</sup>Departamento de Ecología, Facultad de Ciencias, Universidad Católica de la Santísima Concepción, Concepción, 4090541, Chile<br />
<sup>3</sup>Department of Genetics, University of Cambridge, Cambridge, United Kingdom<br />
<sup>4</sup>SNSB-Bavarian State Collection of Zoology, Munich, Germany<br />
<sup>5</sup>University Museum Bergen, University of Bergen, Bergen, Norway<br />
<sup>6</sup>GeoZentrum Nordbayern, Friedrich-Alexander University Erlangen-Nürnberg (FAU), Erlangen, Germany<br />
<sup>7</sup>Department of Biosciences, Swansea University, Swansea, United Kingdom

\*Corresponding author: [kristina.kocakova@pim.uzh.ch](mailto:kristina.kocakova@pim.uzh.ch)

---

## Overview

This repository contains the scripts used to curate and visualise the data in the FINS dataset, available [here](https://shorturl.at/crNeh).


### Repository Structure

- **`data/`**  
  Contains three .xlsx files, which were used to assign valid names to oudtated synonyms and extinct/extant status and higher taxonomy classification to valid taxa.
  The synonym tables were obtained from [Shark References](https://shark-references.com/), with the permission of the curators of the website.


- **`code/`**  
  Contains scripts used to assign information to collections and occurrences within the dataset. This folder also contains scripts used to produce the figures presented in the article.
---

### Usage notes

Minimum and maximum age was originally collected for collections. Based on the collection number, this information was then transfered from collecitons to the appropriate occurrences. This was done in the add_ages_to_occs.py, 
