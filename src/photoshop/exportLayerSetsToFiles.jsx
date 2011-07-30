//***********************************************************************************************
//
// Copyright (C) 2009 - 2011 - Thomas Mansencal - thomas.mansencal@gmail.com
//
//***********************************************************************************************

/**
 * @projectDescription	exportLayerSetsToFiles.jsx - Photoshop CS 3 /4 Export Layer Sets to files script.
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
MATCHING_EXPORT = false
CHANNELS_TYPES = ["Diffuse", "Specular", "Bump"]
SUPPORTED_WIDTHS = [256, "025k", 512, "05k", 1024, "1k", 2048, "2k", 4096, "4k", 8192, "8k", 16384, "16k"];

//***********************************************************************************************
//***	Script classes and functions.
//***********************************************************************************************

/**
 * This function is the main function.
 */
function exportLayerSetsToFiles()
{

	if (app.documents.length <= 0)
	{
		alert("ELtF | Error: There is no active document!");
		return;
	}
	try
	{
		var documentName = activeDocument.fullName;

	}
	catch (e)
	{
		alert("ELtF | Error: The document has not been saved!");
		return;
	}
	if (0 == exportLayerSetsToFiles_UI())
		return;
}

/**
 * This function is the ui function.
 */
function exportLayerSetsToFiles_UI()
{
	margin = 16

	var ui = new Window("dialog", "Export LayerSets To Files");

	var brush = ui.graphics.newBrush(ui.graphics.BrushType.THEME_COLOR, "appDialogBackground");
	ui.graphics.backgroundColor = brush;
	ui.graphics.disabledBackgroundColor = ui.graphics.backgroundColor;
	ui.alignChildren = "fill";

	ui.Export_panel = ui.add("panel");
	ui.Export_panel.orientation = "column";
	ui.Export_panel.alignChildren = "fill";
	ui.Export_panel.margins = margin;
	ui.Export_panel.text = "Export Directory";

	ui.Browse_group = ui.Export_panel.add("group");
	ui.Browse_group.orientation = "row";

	ui.Folder_editText = ui.Browse_group.add("edittext", undefined, "");
	ui.Folder_editText.preferredSize.width = 192;
	ui.Folder_editText.text = new Folder(activeDocument.fullName.parent).fsName;

	ui.Browse_button = ui.Browse_group.add("button", undefined, "...");
	ui.Browse_button.onClick = function()
	{
		exportFolder = new Folder(ui.Folder_editText.text);
		if (exportFolder.exists)
			var selectedFolder = Folder.selectDialog(undefined, exportFolder.fsName);
		else
			var selectedFolder = "/"

		if (selectedFolder != null)
		{
			ui.Folder_editText.text = selectedFolder.fsName;
		}
	}

	ui.Affixes_panel = ui.add("panel");
	ui.Affixes_panel.orientation = "column";
	ui.Affixes_panel.alignChildren = "fill";
	ui.Affixes_panel.margins = margin;
	ui.Affixes_panel.text = "Export Affixes";

	ui.Affixes_group = ui.Affixes_panel.add("group");
	ui.Affixes_group.orientation = "row";

	ui.Affixes_group.add("statictext", undefined, "Prefix:");
	ui.Prefix_editText = ui.Affixes_group.add("edittext", undefined, "");
	ui.Prefix_editText.preferredSize.width = 80;
	var documentName = activeDocument.fullName.name;
	ui.Prefix_editText.text = decodeURI(documentName.substring(0, documentName.indexOf(".")));

	ui.Affixes_group.add("statictext", undefined, "Suffix:");
	ui.Suffix_editText = ui.Affixes_group.add("edittext", undefined, "");
	ui.Suffix_editText.preferredSize.width = 80;
	ui.Suffix_editText.text = getSuffix();

	ui.Format_panel = ui.add("panel");
	ui.Format_panel.orientation = "column";
	ui.Format_panel.alignChildren = "fill";
	ui.Format_panel.margins = margin;
	ui.Format_panel.text = "Export Format";

	ui.Format_group = ui.Format_panel.add("group");
	ui.Format_group.orientation = "row";
	ui.Format_group.spacing = 56;

	ui.Format_group.add("statictext", undefined, "File Format:");
	ui.Tiff_radioButton = ui.Format_group.add("radiobutton", undefined, "Tiff");
	ui.Tiff_radioButton.value = true;
	ui.Jpeg_radioButton = ui.Format_group.add("radiobutton", undefined, "Jpeg");
	ui.Jpeg_radioButton.value = false;

	ui.Modal_group = ui.add("group");
	ui.Modal_group.orientation = "row";
	ui.Modal_group.alignment = "right";

	ui.Export_button = ui.Modal_group.add("button", undefined, "Export");
	ui.Export_button.onClick = function()
	{
		if (ui.Folder_editText.text != "")
		{
			exportFolder = new Folder(ui.Folder_editText.text);
			if (exportFolder.exists)
			{
				if (ui.Tiff_radioButton.value == true)
					exportFormat = getExportOptions("Tiff")
				else
					exportFormat = getExportOptions("Jpeg")
				doExportLayerSetsToFile(CHANNELS_TYPES, exportFormat[0], exportFormat[1], exportFolder, ui.Prefix_editText.text, ui.Suffix_editText.text)
			}
			else
				alert("ELtF | Error: Export directory doesn"t exists!");
		}
		else
			alert("ELtF | Error: You need to choose an export directory!");

	}

	ui.Cancel_button = ui.Modal_group.add("button", undefined, "Cancel");

	ui.center();
	return ui.show();
}

/**
 * This function constructs the exportOptions object.
 *
 * @param	{String}	exportType	"Current export type."
 * @return	{SaveOptions}	"Return a saveOptions object."
 */
function getExportOptions(exportType)
{
	switch (exportType)
	{
		case "Tiff":
			exportOptions = new TiffSaveOptions()
			exportOptions.embedColorProfile = true;
			exportOptions.layers = false
			exportOptions.transparency = false
			extension = "tif"

			exportFormat = [exportOptions, extension]
			return exportFormat

		case "Jpeg":
			exportOptions = new JPEGSaveOptions()
			exportOptions.embedColorProfile = true;
			exportOptions.quality = 12
			extension = "jpg"

			exportFormat = [exportOptions, extension]
			return exportFormat
	}
}

/**
 * This function gets a resolution suffix.
 *
 * @return	{String}	"Return a resolution suffix."
 */
function getSuffix()
{
	width = UnitValue(activeDocument.width.value, ("px"))
	for (i = 0; i < (SUPPORTED_WIDTHS.length); i += 2)
	{
		if (width.value == SUPPORTED_WIDTHS[i])
			return SUPPORTED_WIDTHS[i + 1]
	}
	return ""
}

/**
 * This function exports the layerSets.
 *
 * @param	{StringArray}	channelsTypes	"Current channels types."
 * @param	{SaveOptions}	exportOptions	"Current save options object."
 * @param	{String}	extension	"Current extension."
 * @param	{String}	exportFolder	"Current export folder."
 * @param	{String}	prefix		"Current export prefix."
 * @param	{String}	suffix		"Current export suffix."
 */
function doExportLayerSetsToFile(channelsTypes, exportOptions, extension, exportFolder, prefix, suffix)
{
	var document = activeDocument;

	for (i = 0; i < document.layers.length; i++)
	{
		document.layers[i].visible = false;
	}

	for (i = 0; i < document.layerSets.length; i++)
	{
		document.layerSets[i].visible = false;
	}

	for (i = document.layerSets.length - 1; i >= 0; i--)
	{
		document.layerSets[i].visible = true;
		if (MATCHING_EXPORT)
		{
			for (j = 0; j < (channelsTypes.length); j++)
			{
				if (document.layerSets[i].name.toLowerCase() == channelsTypes[j].toLowerCase())
				{
					file = new File(exportFolder + "/" + prefix + "_" + channelsTypes[j] + "_" + suffix + "." + extension);
					document.saveAs(file, exportOptions, true, Extension.LOWERCASE);
					break;
				}
			}
		}
		else
		{
			file = new File(exportFolder + "/" + prefix + "_" + document.layerSets[i].name + "_" + suffix + "." + extension);
			document.saveAs(file, exportOptions, true, Extension.LOWERCASE);
		}
	}
}

exportLayerSetsToFiles();