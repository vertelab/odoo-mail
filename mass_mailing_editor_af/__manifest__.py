{
    "name": "AF Mass Mailing Snippets",
    "summary": "This version is used to customize the Odoo standard mail body widgets in accordance to 'Af' mail template.",
    "version": "12.0.0.5.22",
    "category": "Email Marketing",
    "description": """
    v12.0.0.0.1 AFC-2067  Added snippets in Mass mailing body.\n
    v12.0.0.0.2 AFC-2067 IMP  Added snippets in Mass mailing body.\n
    v12.0.0.0.3 AFC-2067 IMP  Added snippets in separate section of Mass mailing body.\n
    v12.0.0.0.4 AFC-2067 Fix  Fixed setting menu URL issue.\n
    v12.0.0.0.5 AFC-2067 Fix  Fixed Font and Background issue in Email.\n
    v12.0.0.0.6 AFC-1725 Added some more snippets in Mass mailing body\n
    v12.0.0.0.7 AFC-2725 Changed some style in snippets.\n
    v12.0.0.1.0 AFC-2829 Added empty snippets above and below all templates for drag and drop.\n
    V12.0.0.1.1 AFC-2830 Changed background color to skip inherit color when snippet moving.\n
    V12.0.0.1.2 AFC-3009 It is unable now to come across and drag out the content of snippets.\n
    V12.0.0.1.3 AFC-3066 Fixed a minor bug for background color (till guiden) and (till tipset) snippets.\n
    V12.0.0.2.0 AFC-3208 Added field for internal name of massmailings.\n
    v12.0.0.2.1 AFC-3182 Change text color on link to ensure level of contrast.\n
    v12.0.0.2.2 AFC-3204 Change code to pass validation.\n
    v12.0.0.2.3 AFC-3411 Change link titles \n
    v12.0.0.2.4 AFC-3284 Changed the values of name fields with internal_name fields \n
    v12.0.0.2.5 AFC-3083 Small view change.\n
    v12.0.0.2.6 AFC-3442 Added error popup if user send a mail without selected template in the editor\n
    v12.0.0.3.0 AFC-3437 Added email to filter, removed unused models in selection, removed is customer as default for res.partner.\n
    v12.0.0.4.0 AFC-3416 Improved the dialog box when sending mass_mailings to show how manny mails that will be sent.\n
    v12.0.0.5.0 AFC-3534 Check for emtpy mail list when sending by mail list.\n
    v12.0.0.5.1 AFC-3418 New snippet created(id=s_mail_block_header_af_dark) and some css changes. \n
    v12.0.0.5.2 AFC-3369 New snippet created(id=s_mail_block_header_af_light) \n
    v12.0.0.5.3 AFC-3558 Bug fix concerning overwriting the same button.\n
    v12.0.0.5.4 AFC-3559 Bug fix count the correct amount of recipients in send confirmation.\n
    v12.0.0.5.5 AFC-3560 Bug fix Removed debugging print.\n
    v12.0.0.5.6 AFC-3422 New snippet created(id=s_mail_block_toppyta_mork_text)\n
    v12.0.0.5.7 AFC-3430 Create new snippet(id=s_mail_block_h3_left_aligned_body_text)\n
    v12.0.0.5.8 AFC-3421 New snippet created(id=s_mail_block_toppyta_ljus_text)\n
    v12.0.0.5.9 AFC-3549 Made snippets responsive(id=s_mail_block_header_af_dark, id=s_mail_block_header_af_light).\n
    v12.0.0.5.10 AFC-3427 Create new snippet(id=s_mail_block_h2_centered) \n
    v12.0.0.5.11 AFC-3428 Create new snippet(id=s_mail_block_h2_left_aligned)\n
    v12.0.0.5.12 AFC-3429 Create new snippet(id=s_mail_block_h2_left_aligned_body_text)\n
    v12.0.0.5.13 AFC-3462 Create new snippet(id=s_mail_block_h3_left_aligned_body_text)\n
    v12.0.0.5.14 AFC-3457 Create new snippet(id=s_mail_block_bullet_list)\n
    v12.0.0.5.15 AFC-3425 Create new snippet(id=s_mail_block_top_surface_light_secundary)\n
    v12.0.0.5.16 AFC-3431 Create new snippet(id=s_mail_block_toppyta_h3_button)\n
    v12.0.0.5.17 AFC-3423 Create new snippet(id=s_mail_block_top_surface_light_primary)\n
    v12.0.0.5.18 AFC-3432 Create new snippet(id=s_mail_block_toppyta_h3_text)\n
    v12.0.0.5.19 AFC-3448 Create new snippet(id=s_mail_block_toppyta_h3_checkikon)\n
    v12.0.0.5.20 AFC-3424 Create new snippet(id=s_mail_block_top_surface_dark_primary)\n
    v12.0.0.5.21 AFC-3460 Create new snippet(id=s_mail_block_h3_gray_background_star_icon)\n
    v12.0.0.5.22 AFC-3452 Create new snippet(id=s_mail_block_h3_white_background_link_star_icon)\n
    """,
    "license": "AGPL-3",
    "maintainer": "Vertel AB",
    "author": "Vertel AB",
    "contributors": ["Vertel AB"],
    "depends": [
        "mass_mailing"
    ],
    "data": [
        'views/mass_mailing_views.xml',
        'views/snippets_themes.xml',
        'views/assets.xml'
    ],
    "auto_install": False,
    "installable": True,
}
