//***********************************************************************************************
//
// Copyright (C) 2009 - 2013 - Thomas Mansencal - thomas.mansencal@gmail.com
//
//***********************************************************************************************

/**
 * @projectDescription	toRGB.jsx.
 *
 * MODIFY THIS AT YOUR OWN RISK
 *
 * @author	Thomas Mansencal	thomas.mansencal@gmail.com
 * @os		Windows,  Mac Os X
 * @tasklist	Code comment.
 */

//***********************************************************************************************
//***	Global variables.
//***********************************************************************************************
INPUT_FOLDER = "j:/uap/build/vhclJuggernaut/maya/textures/masters/psd/juggernautComicConAvA_lodA/psd/DISP"
OUTPUT_FOLDER = "j:/uap/build/vhclJuggernaut/maya/textures/masters/psd/processing"
INPUT_FILE_FORMAT = "psd"
OUTPUT_FILE_FORMAT = "tif"

//***********************************************************************************************
//***	Script classes and functions.
//***********************************************************************************************
/**
 * This function constructs the exportOptions object.
 *
 * @param	{String}	exportType	"Current export type."
 * :return	{SaveOptions}	"Return a saveOptions object."
 */
function getExportOptions(exportType)
{
	switch (exportType)
	{
		case "tif":
			exportOptions = new TiffSaveOptions()
			exportOptions.embedColorProfile = true;
			exportOptions.layers = false
			exportOptions.transparency = false
			extension = "tif"

			exportFormat = [exportOptions, extension]
			return exportFormat

		case "jpg":
			exportOptions = new JPEGSaveOptions()
			exportOptions.embedColorProfile = true;
			exportOptions.quality = 12
			extension = "jpg"

			exportFormat = [exportOptions, extension]
			return exportFormat
	}
}

/**
 * This function gets a neutral gray background layer.
 */
function getNeutralGrayBackgroundLayer()
{
	var layer = app.activeDocument.artLayers.add();
	layer.name = "Neutral Gray";
	layer.blendMode = BlendMode.NORMAL;
	var hasBackgroundLayer = false;
	for (i = 0; i < app.activeDocument.layers.length; i++)
			if (app.activeDocument.layers[i].isBackgroundLayer == true)
			{
				hasBackgroundLayer = true
				break;
			}
	if (hasBackgroundLayer)
		index = 2
	else
		index = 1

	layer.move(app.activeDocument.layers[app.activeDocument.layers.length - index], ElementPlacement.PLACEAFTER);
	
	var color = new SolidColor();
	color.rgb.red = 128;
	color.rgb.green = 128;
	color.rgb.blue = 128;
	
	app.activeDocument.selection.selectAll();
	app.activeDocument.selection.fill(color);
}

/**
 * This function RGize stuff.
 */
function toRG()
{
	var inpuFolder = new Folder(INPUT_FOLDER);
	files = inpuFolder.getFiles("*." + INPUT_FILE_FORMAT).sort()
		
	for(i = 0; i < files.length; i++)
	{
		var document  = open(files[i]);

		for (j = 0; j < document.layers.length; j++)
			document.layers[j].visible = false;
		for (j = 0; j < document.layerSets.length; j++)
			document.layerSets[j].visible = false;
		
		getNeutralGrayBackgroundLayer();

		for (j = document.layerSets.length - 1; j >= 0; j--)
		{
			if (document.layerSets[j].name == "DISP" || document.layerSets[j].name == "DISP3")
			{
				document.layerSets[j].visible = true;
				
				if (document.layerSets[j].name == "DISP")
					var affixe = "Lines";
				else
					var affixe = "Panels";
				var name = files[i].name.split(".")[0];
				var outputPath = OUTPUT_FOLDER + "/" + name + "_" + affixe + "." + OUTPUT_FILE_FORMAT;
				file = new File(outputPath);
 				document.saveAs(file, getExportOptions(OUTPUT_FILE_FORMAT)[0], true, Extension.LOWERCASE);
				
				document.layerSets[j].visible = false;
			}	
		}
		document.close(SaveOptions.DONOTSAVECHANGES);
	}
}

/**
 * This function RGBize stuff.
 */
function toRGB()
{
	var document  = app.activeDocument;

	for (i = 0; i < document.layers.length; i++)
		document.layers[i].visible = false;
	for (i = 0; i < document.layerSets.length; i++)
		document.layerSets[i].visible = false;
		
	getNeutralGrayBackgroundLayer();

	for (i = document.layerSets.length - 1; i >= 0; i--)
	{
		var layerSetName = document.layerSets[i].name
		if (layerSetName == "Lines" || layerSetName == "Panels" || layerSetName == "Extras")
		{
			document.layerSets[i].visible = true;
			var name = app.activeDocument.name.split(".")[0];
			var outputPath = OUTPUT_FOLDER + "/" + name + "_" + layerSetName + "." + OUTPUT_FILE_FORMAT;
			file = new File(outputPath);
 			document.saveAs(file, getExportOptions(OUTPUT_FILE_FORMAT)[0], true, Extension.LOWERCASE);
			document.layerSets[i].visible = false;
		}	
	}
}

toRGB();
