//***********************************************************************************************
//
// Copyright (C) 2009 - 2011 - Thomas Mansencal - thomas.mansencal@gmail.com
//
//***********************************************************************************************

/**
 * @projectDescription	exportLayerSetsToFiles.jsx - Photoshop CS 3 /4 Export Layer Sets To Files Script.
 *
 * MODIFY THIS AT YOUR OWN RISK
 *
 * @author	Thomas Mansencal	thomas.mansencal@gmail.com
 * @os		Windows,  Mac Os X
 * @tasklist	Code Comment.
 */
//***********************************************************************************************
//***	Javascript Begin
//***********************************************************************************************

//***********************************************************************************************
//***	Global Variables
//***********************************************************************************************
MATCHING_EXPORT = false
CHANNELS_TYPES = ["Diffuse", "Specular", "Bump"]
SUPPORTED_WIDTHS = [256, "025k", 512, "05k", 1024, "1k", 2048, "2k", 4096, "4k", 8192, "8k", 16384, "16k"];

//***********************************************************************************************
//***	Script Classes And Functions
//***********************************************************************************************

/**
 * This Function Is The Main Function.
 */
function exportLayerSetsToFiles()
{


	if (app.documents.length <= 0)
	{
		alert("ELtF | Error: There Is No Active Document!");
		return;
	}
	try
	{
		var documentName = activeDocument.fullName;

	}
	catch (e)
	{
		alert("ELtF | Error: The Document Has Not Been Saved!");
		return;
	}
	if (0 == exportLayerSetsToFiles_UI())
		return;
}

/**
 * This Function Is The UI Function.
 */
function exportLayerSetsToFiles_UI()
{
	margin = 16

	var ui = new Window("dialog", "Export LayerSets To Files");

	var brush = ui.graphics.newBrush(ui.graphics.BrushType.THEME_COLOR, "appDialogBackground");
	ui.graphics.backgroundColor = brush;
	ui.graphics.disabledBackgroundColor = ui.graphics.backgroundColor;
	ui.alignChildren = 'fill';

	ui.Export_Panel = ui.add('panel');
	ui.Export_Panel.orientation = 'column';
	ui.Export_Panel.alignChildren = 'fill';
	ui.Export_Panel.margins = margin;
	ui.Export_Panel.text = "Export Directory";

	ui.Browse_Group = ui.Export_Panel.add("group");
	ui.Browse_Group.orientation = 'row';

	ui.Folder_EditText = ui.Browse_Group.add("edittext", undefined, "");
	ui.Folder_EditText.preferredSize.width = 192;
	ui.Folder_EditText.text = new Folder(activeDocument.fullName.parent).fsName;

	ui.Browse_Button = ui.Browse_Group.add("button", undefined, "...");
	ui.Browse_Button.onClick = function()
	{
		exportFolder = new Folder(ui.Folder_EditText.text);
		if (exportFolder.exists)
			var selectedFolder = Folder.selectDialog(undefined, exportFolder.fsName);
		else
			var selectedFolder = "/"

		if (selectedFolder != null)
		{
			ui.Folder_EditText.text = selectedFolder.fsName;
		}
	}

	ui.Affixes_Panel = ui.add('panel');
	ui.Affixes_Panel.orientation = 'column';
	ui.Affixes_Panel.alignChildren = 'fill';
	ui.Affixes_Panel.margins = margin;
	ui.Affixes_Panel.text = "Export Affixes";

	ui.Affixes_Group = ui.Affixes_Panel.add("group");
	ui.Affixes_Group.orientation = 'row';

	ui.Affixes_Group.add("statictext", undefined, "Prefix:");
	ui.Prefix_EditText = ui.Affixes_Group.add("edittext", undefined, "");
	ui.Prefix_EditText.preferredSize.width = 80;
	var documentName = activeDocument.fullName.name;
	ui.Prefix_EditText.text = decodeURI(documentName.substring(0, documentName.indexOf(".")));

	ui.Affixes_Group.add("statictext", undefined, "Suffix:");
	ui.Suffix_EditText = ui.Affixes_Group.add("edittext", undefined, "");
	ui.Suffix_EditText.preferredSize.width = 80;
	ui.Suffix_EditText.text = getSuffix();

	ui.Format_Panel = ui.add('panel');
	ui.Format_Panel.orientation = 'column';
	ui.Format_Panel.alignChildren = 'fill';
	ui.Format_Panel.margins = margin;
	ui.Format_Panel.text = "Export Format";

	ui.Format_Group = ui.Format_Panel.add("group");
	ui.Format_Group.orientation = 'row';
	ui.Format_Group.spacing = 56;

	ui.Format_Group.add("statictext", undefined, "File Format:");
	ui.Tiff_RadioButton = ui.Format_Group.add("radiobutton", undefined, "Tiff");
	ui.Tiff_RadioButton.value = true;
	ui.Jpeg_RadioButton = ui.Format_Group.add("radiobutton", undefined, "Jpeg");
	ui.Jpeg_RadioButton.value = false;

	ui.Modal_Group = ui.add("group");
	ui.Modal_Group.orientation = 'row';
	ui.Modal_Group.alignment = 'right';

	ui.Export_Button = ui.Modal_Group.add("button", undefined, "Export");
	ui.Export_Button.onClick = function()
	{
		if (ui.Folder_EditText.text != "")
		{
			exportFolder = new Folder(ui.Folder_EditText.text);
			if (exportFolder.exists)
			{
				if (ui.Tiff_RadioButton.value == true)
					exportFormat = getExportOptions("Tiff")
				else
					exportFormat = getExportOptions("Jpeg")
				doExportLayerSetsToFile(CHANNELS_TYPES, exportFormat[0], exportFormat[1], exportFolder, ui.Prefix_EditText.text, ui.Suffix_EditText.text)
			}
			else
				alert("ELtF | Error: Export Directory Doesn't Exists!");
		}
		else
			alert("ELtF | Error: You Need To Choose An Export Directory!");

	}

	ui.Cancel_Button = ui.Modal_Group.add("button", undefined, "Cancel");

	ui.center();
	return ui.show();
}

/**
 * This Function Constructs The ExportOptions Object.
 *
 * @param	{String}	exportType	"Current Export Type."
 * @return	{SaveOptions}	"Return A SaveOptions Object."
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
 * This Function Gets A Resolution Suffix.
 *
 * @return	{String}	"Return A Resolution Suffix."
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
 * This Function Exports The LayerSets.
 *
 * @param	{StringArray}	channelsTypes	"Current Channels Types."
 * @param	{SaveOptions}	exportOptions	"Current Save Options Object."
 * @param	{String}	extension	"Current Extension."
 * @param	{String}	exportFolder	"Current Export Folder."
 * @param	{String}	prefix		"Current Export Prefix."
 * @param	{String}	suffix		"Current Export Suffix."
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

//***********************************************************************************************
//***	Javascript End
//***********************************************************************************************
