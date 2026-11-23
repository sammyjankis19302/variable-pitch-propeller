# CAD: two hubs in SolidWorks

*[← back to the project](../README.md)*

The hub went through two versions in three weeks. Both are SolidWorks 2024 files: open them with
SolidWorks 2024 or later, or with the free eDrawings viewer. The pictures below are the previews
stored inside the files themselves, pulled out with [`tools/sw_preview.py`](../tools/sw_preview.py).

![how the linkage works](../figures/pitch-mechanism.png)

## Version 1: three blades (24–25 May 2025)

A round hub with three blade sockets, a plate below it that slides along the shaft, and a link from
the plate to each blade root. The blade was lofted from the OpenProp sections.

<table>
<tr>
<td align="center"><img src="previews/v1-total-hub.png" width="180"><br><sub><code>TOTAL HUB.SLDASM</code><br>the assembly</sub></td>
<td align="center"><img src="previews/v1-hub.png" width="180"><br><sub><code>hub</code><br>three sockets</sub></td>
<td align="center"><img src="previews/v1-pitch-controller.png" width="180"><br><sub><code>pitch controller</code><br>the sliding plate</sub></td>
<td align="center"><img src="previews/v1-coupler.png" width="180"><br><sub><code>coupler</code><br>holds a blade root</sub></td>
</tr>
<tr>
<td align="center"><img src="previews/v1-string.png" width="180"><br><sub><code>string</code><br>the link</sub></td>
<td align="center"><img src="previews/v1-shaft.png" width="180"><br><sub><code>shaft</code></sub></td>
<td align="center"><img src="previews/v1-trial-1-blade.png" width="180"><br><sub><code>trial 1 blade</code><br>lofted from OpenProp</sub></td>
<td align="center"><img src="../media/cad-three-blade.jpg" width="180"><br><sub>the whole propeller</sub></td>
</tr>
</table>

<p align="center"><img src="../media/cad-three-blade-pitch.gif" width="70%"><br>
<sub>25 May 2025: turning the pitch mate of the three-blade assembly through its range in SolidWorks.</sub></p>

## Version 2: two blades (31 May – 11 June 2025)

Two blades instead of three, a block-shaped hub, and a cross-shaped controller with a link to each
blade. This is the version we printed and put on the bench.

<table>
<tr>
<td align="center"><img src="previews/v2-assem1.png" width="180"><br><sub><code>Assem1.SLDASM</code><br>the assembly</sub></td>
<td align="center"><img src="previews/v2-hub.png" width="180"><br><sub><code>hub</code><br>two sockets</sub></td>
<td align="center"><img src="previews/v2-hub1.png" width="180"><br><sub><code>hub1</code></sub></td>
<td align="center"><img src="previews/v2-cont.png" width="180"><br><sub><code>CONT</code><br>the controller</sub></td>
</tr>
<tr>
<td align="center"><img src="previews/v2-coupler.png" width="180"><br><sub><code>coupler</code><br>holds a blade root</sub></td>
<td align="center"><img src="previews/v2-string.png" width="180"><br><sub><code>string</code><br>the link</sub></td>
<td align="center"><img src="previews/v2-bolt1.png" width="180"><br><sub><code>bolt1</code></sub></td>
<td align="center"><img src="previews/v2-bolt2.png" width="180"><br><sub><code>bolt2</code></sub></td>
</tr>
</table>

<p align="center"><img src="../media/cad-two-blade-pitch.gif" width="55%"><br>
<sub>Setting the blade angle of the two-blade assembly in SolidWorks (a screen recording,
<a href="../media/videos/03-cad-two-blade-angle-mate.mp4">full clip</a>).</sub></p>

The blades are our OpenProp design. `Propeller 10x45.SLDPRT` is the two-blade propeller; the assembly
uses its blade as a separate part, `10x45_wing`, which is not in this folder, so SolidWorks will report
that part as missing when it opens `Assem1.SLDASM`.

## Other files

* The sixteen blade-angle models used for the CFD are in [`cfd/models/`](../cfd/models/), next to what came
  out of them.
* The APC 12×6 model, a catalogue propeller we only tried in Flow Simulation, is not ours to share.
