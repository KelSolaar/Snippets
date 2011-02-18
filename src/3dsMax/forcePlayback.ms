fn forcePlayback lookForward =
(
	startTime = sliderTime
	do sliderTime = ( sliderTime + 1 ) while sliderTime <= startTime + lookForward
)

forcePlayback(150)