# AndroidTV

Guida TV italiana (XMLTV) per OwnTV, con gli ID dei canali riscritti per combaciare con la playlist.

- Fonte: guide pubbliche di [iptv-epg.org](https://iptv-epg.org/files/epg-it.xml).
- `remap_epg.py` riscrive gli ID (es. `Canale.5.it` diventa `Canale5.it`) in base a `ids.txt`.
- Un'azione GitHub (`.github/workflows/update-epg.yml`) rigenera il file ogni giorno e lo pubblica sul ramo `epg`.

URL da incollare in OwnTV (Impostazioni → Sorgenti e guida → Fonti EPG):

```
https://raw.githubusercontent.com/cocix-it/AndroidTV/epg/epg_it.xml.gz
```

`ids.txt` contiene i `tvg-id` della playlist: va aggiornato a mano se la playlist cambia.
