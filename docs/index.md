---
layout: default
title: Home
---

<!-- Important links -->
<div style="text-align: center;">
    <ul style="list-style: none; display: inline; margin: 0 auto; padding: 0;">
        {% for link in site.links %}
        <li style="display: inline-block; margin: 0px 20px;">
            <a href="{{ link.url }}"><img src="{{ link.icon | relative_url }}"/></a>
            <h4 style="margin: 0; padding: 0;">{{ link.name }}</h4>
        </li>
        {% endfor %}
    </ul>
</div>
    

The NES Video-Music Database (NES-MVDB) is a dataset of 98,940 short (15 seconds) gameplay videos from 386 NES games, each paired with its original music piece in symbolic format (MIDI). NES-MVDB is built upon the Nintendo Entertainment System Music Database (NES-MDB).

### Examples
---

### Dataset structure
---

The dataset is organized into 4 directories:
- **Midi**: midi files from NES-MDB
- **Audio**: midi files from NES-MDB synthesized as MP3 with the original NES synth
- **Videos**: gameplay videos organized by game id, and sliced in fragments of 15 seconds
- **Video-Midi**: a csv file with the game id, name, and metadata of each game in the dataset

### Citing this work
---

If you use the NES-vmDB dataset in your work, please cite the paper where it was introduced:

```
@article{cardoso2024nes,
  title={The NES Video-Music Database: A Dataset of Symbolic Video Game Music Paired with Gameplay Videos},
  author={Cardoso, Igor and Moraes, Rubens O and Ferreira, Lucas N},
  journal={arXiv preprint arXiv:2404.04420},
  year={2024}
}
```

