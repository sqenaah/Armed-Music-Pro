from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.errors import MessageNotModified
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from ArmedMusic import app
from ArmedMusic.utils.database import (
    add_nonadmin_chat,
    get_authuser,
    get_authuser_names,
    get_playmode,
    get_playtype,
    get_upvote_count,
    is_nonadmin_chat,
    is_skipmode,
    remove_nonadmin_chat,
    set_playmode,
    set_playtype,
    set_upvotes,
    skip_off,
    skip_on,
)
from ArmedMusic.utils.decorators.admins import ActualAdminCB
from ArmedMusic.utils.decorators.language import language, languageCB
from ArmedMusic.utils.inline.settings import (
    auth_users_markup,
    playmode_users_markup,
    setting_markup,
    vote_mode_markup,
)
from ArmedMusic.utils.inline.start import private_panel
from config import BANNED_USERS, OWNER_ID


@app.on_message(
    filters.command(["settings", "setting"]) & filters.group & ~BANNED_USERS
)
@language
async def settings_mar(client, message: Message, _):
    buttons = setting_markup(_)
    await message.reply_text(
        _["setting_1"].format(app.mention, message.chat.id, message.chat.title),
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_callback_query(filters.regex("settings_helper") & ~BANNED_USERS)
@languageCB
async def settings_cb(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer(_["set_cb_8"])
    except:
        pass
    buttons = setting_markup(_)
    try:
        return await CallbackQuery.edit_message_text(
            _["setting_1"].format(
                app.mention,
                CallbackQuery.message.chat.id,
                CallbackQuery.message.chat.title,
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    except MessageNotModified:
        return


@app.on_callback_query(filters.regex("settingsback_helper") & ~BANNED_USERS)
@languageCB
async def settings_back_markup(client, CallbackQuery: CallbackQuery, _):
    try:
        await CallbackQuery.answer()
    except:
        pass
    if CallbackQuery.message.chat.type == ChatType.PRIVATE:
        buttons = private_panel(_)
        try:
            return await CallbackQuery.edit_message_text(
                _["start_2"].format(CallbackQuery.from_user.mention, app.mention),
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        except MessageNotModified:
            return
    else:
        buttons = setting_markup(_)
        try:
            return await CallbackQuery.edit_message_reply_markup(
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        except MessageNotModified:
            return


@app.on_callback_query(
    filters.regex(
        pattern=r"^(SEARCHANSWER|PLAYMODEANSWER|PLAYTYPEANSWER|AUTHANSWER|ANSWERVOMODE|VOTEANSWER|PM|AU|VM)$"
    )
    & ~BANNED_USERS
)
@languageCB
async def without_Admin_rights(client, CallbackQuery, _):
    command = CallbackQuery.matches[0].group(1)

    if command == "SEARCHANSWER":
        try:
            return await CallbackQuery.answer(_["setting_2"], show_alert=True)
        except:
            return
    if command == "PLAYMODEANSWER":
        try:
            return await CallbackQuery.answer(_["setting_5"], show_alert=True)
        except:
            return
    if command == "PLAYTYPEANSWER":
        try:
            return await CallbackQuery.answer(_["setting_6"], show_alert=True)
        except:
            return
    if command == "AUTHANSWER":
        try:
            return await CallbackQuery.answer(_["setting_3"], show_alert=True)
        except:
            return
    if command == "VOTEANSWER":
        try:
            return await CallbackQuery.answer(_["setting_8"], show_alert=True)
        except:
            return
    if command == "ANSWERVOMODE":
        current = await get_upvote_count(CallbackQuery.message.chat.id)
        try:
            return await CallbackQuery.answer(_["setting_9"].format(current), show_alert=True)
        except:
            return

    chat_id = CallbackQuery.message.chat.id
    if command == "PM":
        try:
            await CallbackQuery.answer(_["set_cb_4"], show_alert=True)
        except:
            pass
        playmode = await get_playmode(chat_id)
        Direct = playmode == "Direct"
        Group = not await is_nonadmin_chat(chat_id)
        Playtype = (await get_playtype(chat_id)) != "Everyone"
        buttons = playmode_users_markup(_, Direct, Group, Playtype)
    elif command == "AU":
        try:
            await CallbackQuery.answer(_["set_cb_3"], show_alert=True)
        except:
            pass
        Group = not await is_nonadmin_chat(chat_id)
        buttons = auth_users_markup(_, Group)
    elif command == "VM":
        mode = await is_skipmode(chat_id)
        current = await get_upvote_count(chat_id)
        buttons = vote_mode_markup(_, current, mode)

    try:
        return await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except MessageNotModified:
        return


@app.on_callback_query(filters.regex("FERRARIUDTI") & ~BANNED_USERS)
@ActualAdminCB
async def addition(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer(_["set_cb_6"], show_alert=True)
    except:
        pass
    chat_id = CallbackQuery.message.chat.id
    if not await is_skipmode(chat_id):
        return await CallbackQuery.answer(_["setting_10"], show_alert=True)

    current = await get_upvote_count(chat_id)
    mode = CallbackQuery.matches[0].group(1)
    final = max(current - 2, 2) if mode == "M" else min(current + 2, 15)
    await set_upvotes(chat_id, final)
    buttons = vote_mode_markup(_, final, True)
    try:
        return await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except MessageNotModified:
        return


@app.on_callback_query(
    filters.regex(pattern=r"^(MODECHANGE|CHANNELMODECHANGE|PLAYTYPECHANGE)$")
    & ~BANNED_USERS
)
@ActualAdminCB
async def playmode_ans(client, CallbackQuery, _):
    command = CallbackQuery.matches[0].group(1)
    try:
        await CallbackQuery.answer(_["set_cb_6"], show_alert=True)
    except:
        pass
    chat_id = CallbackQuery.message.chat.id

    if command == "CHANNELMODECHANGE":
        if await is_nonadmin_chat(chat_id):
            await remove_nonadmin_chat(chat_id)
        else:
            await add_nonadmin_chat(chat_id)
    elif command == "MODECHANGE":
        playmode = await get_playmode(chat_id)
        await set_playmode(chat_id, "Inline" if playmode == "Direct" else "Direct")
    elif command == "PLAYTYPECHANGE":
        playty = await get_playtype(chat_id)
        await set_playtype(chat_id, "Admin" if playty == "Everyone" else "Everyone")

    playmode = await get_playmode(chat_id)
    Group = not await is_nonadmin_chat(chat_id)
    Playtype = (await get_playtype(chat_id)) != "Everyone"
    Direct = playmode == "Direct"
    buttons = playmode_users_markup(_, Direct, Group, Playtype)
    try:
        return await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except MessageNotModified:
        return


@app.on_callback_query(filters.regex(pattern=r"^(AUTH|AUTHLIST)$") & ~BANNED_USERS)
@ActualAdminCB
async def authusers_mar(client, CallbackQuery, _):
    command = CallbackQuery.matches[0].group(1)
    chat_id = CallbackQuery.message.chat.id

    if command == "AUTHLIST":
        _authusers = await get_authuser_names(chat_id)
        if not _authusers:
            try:
                return await CallbackQuery.answer(_["setting_4"], show_alert=True)
            except:
                return
        try:
            await CallbackQuery.answer(_["set_cb_7"], show_alert=True)
        except:
            pass
        msg = _["auth_7"].format(CallbackQuery.message.chat.title)
        j = 0
        for note in _authusers:
            _note = await get_authuser(chat_id, note)
            user_id = _note["auth_user_id"]
            admin_id = _note["admin_id"]
            admin_name = _note["admin_name"]
            try:
                user = await app.get_users(user_id)
                user = user.first_name
                j += 1
            except:
                continue
            msg += f"{j}❍ {user}[<code>{user_id}</code>]\n"
            msg += f"   {_['auth_8']} {admin_name}[<code>{admin_id}</code>]\n\n"
        upl = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="AU"),
                InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close"),
            ]]
        )
        try:
            return await CallbackQuery.edit_message_text(msg, reply_markup=upl)
        except MessageNotModified:
            return

    try:
        await CallbackQuery.answer(_["set_cb_6"], show_alert=True)
    except:
        pass
    if await is_nonadmin_chat(chat_id):
        await remove_nonadmin_chat(chat_id)
        buttons = auth_users_markup(_, True)
    else:
        await add_nonadmin_chat(chat_id)
        buttons = auth_users_markup(_)
    try:
        return await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except MessageNotModified:
        return


@app.on_callback_query(filters.regex("VOMODECHANGE") & ~BANNED_USERS)
@ActualAdminCB
async def vote_change(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer(_["set_cb_6"], show_alert=True)
    except:
        pass
    chat_id = CallbackQuery.message.chat.id
    if await is_skipmode(chat_id):
        await skip_off(chat_id)
    else:
        await skip_on(chat_id)
    current = await get_upvote_count(chat_id)
    buttons = vote_mode_markup(_, current, await is_skipmode(chat_id))
    try:
        return await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except MessageNotModified:
        return
